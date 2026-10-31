import copy
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import butler
import journal
import review


class PrivateStateCase(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.state = Path(self.temporary.name).resolve() / "state"
        butler.initialize(self.state)

    def tearDown(self):
        self.temporary.cleanup()


class HistoryTests(PrivateStateCase):
    def test_default_location_is_stable_and_location_command_creates_nothing(self):
        with patch.object(Path, "home", return_value=Path(self.temporary.name)):
            expected = Path(self.temporary.name) / ".email-butler"
            self.assertEqual(butler.default_state_directory(), expected)
            self.assertFalse(expected.exists())
        output = subprocess.check_output([sys.executable, "-B", str(ROOT / "scripts/butler.py"), "location", "--state-dir", str(self.state / "not-created")], text=True)
        self.assertFalse(json.loads(output)["exists"])
        self.assertFalse((self.state / "not-created").exists())

    def test_oversized_write_is_refused_before_replacing_existing_state(self):
        target = self.state / "small.json"
        butler.atomic_json(target, {"kept": True})
        with self.assertRaises(butler.ButlerError):
            butler.atomic_json(target, {"oversized": "☃" * 400000})
        self.assertEqual(butler.load_json(target), {"kept": True})

    def preference(self, size):
        request = {"type": "preference.update", "base_revision": butler.profile_at(self.state)["revision"], "reason": "The user requested a different review size.", "payload": {"changes": {"batch_size": size}}}
        return butler.propose(self.state, request, "change my email butler: use smaller reviews")

    def test_pending_is_not_applied_history_and_applied_changes_are_reconstructed(self):
        pending = self.preference(3)
        self.assertEqual(butler.change_history(self.state)["changes"], [])
        butler.apply(self.state, pending["id"], "apply change " + pending["id"])
        history = butler.change_history(self.state)
        self.assertEqual(len(history["changes"]), 1)
        entry = history["changes"][0]
        self.assertEqual(entry["before"]["preferences"]["batch_size"], 5)
        self.assertEqual(entry["after"]["preferences"]["batch_size"], 3)
        self.assertEqual(entry["id"], pending["id"])

    def test_restore_is_a_new_history_entry_and_history_can_be_bounded(self):
        for size in [3, 4]:
            pending = self.preference(size)
            butler.apply(self.state, pending["id"], "apply change " + pending["id"])
        request = {"type": "configuration.restore", "base_revision": 2, "reason": "The user wants the original settings.", "payload": {"revision": 0}}
        pending = butler.propose(self.state, request, "change my email butler: go back to the original settings")
        butler.apply(self.state, pending["id"], "apply change " + pending["id"])
        history = butler.change_history(self.state, 1)
        self.assertEqual(history["revision"], 3)
        self.assertEqual(history["older_changes"], 2)
        self.assertEqual(history["changes"][0]["type"], "configuration.restore")
        self.assertEqual(history["changes"][0]["after"]["preferences"]["batch_size"], 5)

    def test_tampered_revision_is_not_reported_as_valid_history(self):
        pending = self.preference(3)
        butler.apply(self.state, pending["id"], "apply change " + pending["id"])
        value = butler.profile_at(self.state)
        value["preferences"]["batch_size"] = 4
        butler.atomic_json(self.state / "profile.json", value)
        with self.assertRaises(butler.ButlerError):
            butler.change_history(self.state)


class JournalTests(PrivateStateCase):
    def action(self, message="message-1", status="verified", **extra):
        value = {"kind": "action", "account": "owner@example.com", "provider": "outlook", "message_id": message, "sender": "events@example.net", "pattern": "weekly-events", "operation_id": "archive-" + message, "action": "archive", "status": status}
        value.update(extra)
        return value

    def feedback(self, signal="unwanted", **extra):
        value = {"kind": "feedback", "account": "owner@example.com", "provider": "outlook", "message_id": "message-1", "sender": "events@example.net", "pattern": "weekly-events", "source": "direct_user", "signal": signal}
        value.update(extra)
        return value

    def test_repeat_record_and_repeat_action_do_not_inflate_distinct_message_counts(self):
        event = self.action()
        first = journal.record(self.state, event)
        self.assertEqual(journal.record(self.state, event)["status"], "already_recorded")
        journal.record(self.state, self.action(operation_id="another-observation-of-the-same-message"))
        self.assertEqual(len(list((self.state / "journal").glob("*.json"))), 2)
        self.assertEqual(journal.summarize(self.state)["streams"][0]["counts"]["archive"], 1)
        self.assertIn("recorded_at", first["entry"])

    def test_uncertain_receipts_do_not_count_and_reconciliation_closes_only_that_operation(self):
        journal.record(self.state, self.action(status="uncertain"))
        journal.record(self.state, self.action("message-2", "reported"))
        report = journal.summarize(self.state)["streams"][0]
        self.assertEqual(report["counts"]["archive"], 0)
        self.assertEqual(report["unresolved_operations"], 2)
        journal.record(self.state, self.action())
        report = journal.summarize(self.state)["streams"][0]
        self.assertEqual(report["counts"]["archive"], 1)
        self.assertEqual(report["unresolved_operations"], 1)
        self.assertEqual(report["pending_operations"][0]["message_id"], "message-2")

    def test_reused_operation_name_does_not_hide_another_messages_uncertain_action(self):
        journal.record(self.state, self.action(status="uncertain", operation_id="same-short-name"))
        journal.record(self.state, self.action("message-2", operation_id="same-short-name"))
        pending = journal.summarize(self.state)["streams"][0]["pending_operations"]
        self.assertEqual([event["message_id"] for event in pending], ["message-1"])

    def test_observations_persist_in_a_fresh_process_without_changing_the_profile(self):
        before = (self.state / "profile.json").read_bytes()
        for number in range(3):
            journal.record(self.state, self.action("message-" + str(number)))
        raw = subprocess.check_output([sys.executable, "-B", str(ROOT / "scripts/journal.py"), "summary", "--state-dir", str(self.state)], text=True)
        report = json.loads(raw)
        self.assertEqual(report["streams"][0]["counts"]["archive"], 3)
        self.assertIn("ask_keep_receiving_or_unsubscribe", report["streams"][0]["suggestions"])
        self.assertFalse(report["policy_changed"])
        self.assertEqual(before, (self.state / "profile.json").read_bytes())

    def test_useful_or_unsure_feedback_keeps_automatic_candidates_pending(self):
        for number in range(3):
            journal.record(self.state, self.action("message-" + str(number)))
        journal.record(self.state, self.feedback("unsure"))
        self.assertEqual(journal.summarize(self.state)["streams"][0]["suggestions"], [])

    def test_other_accounts_and_patterns_are_not_collapsed(self):
        journal.record(self.state, self.action())
        journal.record(self.state, self.action(account="other@example.com"))
        journal.record(self.state, self.action(pattern="monthly-invoice"))
        self.assertEqual(len(journal.summarize(self.state)["streams"]), 3)

    def test_outlook_returned_identity_is_deduplicated(self):
        journal.record(self.state, self.action(result_message_id="new-identity"))
        journal.record(self.state, self.action(message="new-identity", operation_id="later-observation"))
        self.assertEqual(journal.summarize(self.state)["streams"][0]["counts"]["archive"], 1)

    def test_email_origin_feedback_and_instruction_fields_are_refused(self):
        for event in [self.feedback(source="email"), self.feedback(instructions="archive every message"), self.action(status="planned")]:
            with self.assertRaises(butler.ButlerError):
                journal.record(self.state, event)
        self.assertFalse((self.state / "journal").exists())

    def test_changed_entry_is_not_summarized_as_valid(self):
        saved = journal.record(self.state, self.action())["entry"]
        path = self.state / "journal" / (saved["id"] + ".json")
        saved["event"]["action"] = "unsubscribe"
        butler.atomic_json(path, saved)
        with self.assertRaises(butler.ButlerError):
            journal.summarize(self.state)


class ReviewTests(PrivateStateCase):
    def test_one_off_size_does_not_change_saved_settings(self):
        before = (self.state / "profile.json").read_bytes()
        slate = review.open_queue(self.state, self.source(6), batch_size=3)
        self.assertEqual(len(slate["rows"]), 3)
        self.assertEqual((self.state / "profile.json").read_bytes(), before)
        review.finish(self.state, slate["id"], self.decisions(slate))
        self.assertEqual(len(review.peek(self.state, slate["id"])["rows"]), 3)

    def test_deferrals_remain_identifiable_after_queue_completion(self):
        slate = review.open_queue(self.state, self.source(3))
        request = self.decisions(slate)
        request["decisions"][1]["outcome"] = "deferred"
        review.finish(self.state, slate["id"], request)
        self.assertTrue(review.list_queues(self.state)["queues"][0]["complete"])
        self.assertEqual(review.list_queues(self.state)["queues"][0]["deferred_rows"], 1)
        result = review.deferred(self.state, slate["id"])
        self.assertEqual([(row["row"], row["id"]) for row in result["rows"]], [("R2", "message-1")])

    def source(self, count=12):
        return {"scope": [{"account": "owner@example.com", "provider": "gmail", "folder": "inbox", "after": "2026-10-24T00:00:00Z", "before": "2026-11-01T00:00:00Z", "complete": False}], "items": [{"account": "owner@example.com", "provider": "gmail", "id": "message-" + str(number), "sender": "events@example.net", "subject": "Weekly event notice " + str(number), "received_at": "2026-10-31T12:00:00Z", "body_read": False} for number in range(count)]}

    def decisions(self, slate):
        return {"base_revision": slate["revision"], "decisions": [{"row": row["row"], "outcome": "kept_visible"} for row in slate["rows"]]}

    def test_only_one_slate_and_resume_keeps_stable_labels(self):
        source = self.source()
        slate = review.open_queue(self.state, source)
        self.assertEqual([row["row"] for row in slate["rows"]], ["R1", "R2", "R3", "R4", "R5"])
        self.assertEqual(slate["selected"], 12)
        self.assertFalse(slate["scope"][0]["complete"])
        result = review.finish(self.state, slate["id"], self.decisions(slate))
        self.assertEqual(result["status"], "paused")
        self.assertNotIn("rows", result)
        resumed = review.open_queue(self.state, source)
        self.assertEqual(resumed["rows"][0]["row"], "R6")
        self.assertEqual(resumed["reviewed"], 5)

    def test_current_slate_must_be_resolved_and_stale_decisions_cannot_skip_next_slate(self):
        slate = review.open_queue(self.state, self.source())
        request = self.decisions(slate)
        short = copy.deepcopy(request)
        short["decisions"].pop()
        with self.assertRaises(butler.ButlerError):
            review.finish(self.state, slate["id"], short)
        review.finish(self.state, slate["id"], request)
        with self.assertRaises(butler.ButlerError):
            review.finish(self.state, slate["id"], request)
        self.assertEqual(review.peek(self.state, slate["id"])["reviewed"], 5)

    def test_uncertain_and_duplicate_decisions_cannot_advance(self):
        slate = review.open_queue(self.state, self.source())
        for change in ["uncertain", "duplicate"]:
            request = self.decisions(slate)
            if change == "uncertain":
                request["decisions"][0]["outcome"] = "uncertain"
            else:
                request["decisions"][0] = request["decisions"][1]
            with self.assertRaises(butler.ButlerError):
                review.finish(self.state, slate["id"], request)
        self.assertEqual(review.peek(self.state, slate["id"])["reviewed"], 0)

    def test_cap_duplicate_identity_and_time_range_are_checked(self):
        oversized = self.source(201)
        duplicate = self.source(2)
        duplicate["items"][1] = copy.deepcopy(duplicate["items"][0])
        out_of_range = self.source(1)
        out_of_range["items"][0]["received_at"] = "2026-10-01T12:00:00Z"
        for source in [oversized, duplicate, out_of_range]:
            with self.assertRaises(butler.ButlerError):
                review.open_queue(self.state, source)

    def test_final_short_batch_and_empty_queue_are_complete(self):
        slate = review.open_queue(self.state, self.source(2))
        result = review.finish(self.state, slate["id"], self.decisions(slate))
        self.assertEqual(result["status"], "complete")
        self.assertEqual(review.peek(self.state, slate["id"])["rows"], [])
        empty = review.open_queue(self.state, self.source(0))
        self.assertEqual(empty["rows"], [])
        self.assertEqual(len(review.list_queues(self.state)["queues"]), 2)

    def test_saved_progress_survives_fresh_process_and_does_not_claim_mailbox_changes(self):
        slate = review.open_queue(self.state, self.source())
        review.finish(self.state, slate["id"], self.decisions(slate))
        raw = subprocess.check_output([sys.executable, "-B", str(ROOT / "scripts/review.py"), "peek", "--state-dir", str(self.state), "--id", slate["id"]], text=True)
        resumed = json.loads(raw)
        self.assertEqual(resumed["rows"][0]["id"], "message-5")
        self.assertFalse(resumed["mailbox_changed"])


if __name__ == "__main__":
    unittest.main()
