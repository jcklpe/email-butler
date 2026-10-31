from pathlib import Path
import sys
import tempfile
import unittest
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import butler
import capabilities
import package_skill


class ChangeTests(unittest.TestCase):
    def setUp(self):
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.state = Path(self.temporary.name).resolve() / "state"
        butler.initialize(self.state)

    def request(self, changes=None, revision=None):
        return {
            "type": "preference.update",
            "base_revision": butler.profile_at(self.state)["revision"] if revision is None else revision,
            "reason": "The user requested a shorter review.",
            "payload": {"changes": changes if changes is not None else {"batch_size": 3}},
        }

    def propose(self, request=None):
        return butler.propose(self.state, self.request() if request is None else request, "change my email butler: shorter reviews")

    def activate(self, proposal):
        return butler.apply(self.state, proposal["id"], "apply change " + proposal["id"])

    def test_proposal_does_not_activate(self):
        proposal = self.propose()
        self.assertEqual(butler.profile_at(self.state)["preferences"]["batch_size"], 5)
        self.assertEqual(proposal["proposed"]["preferences"]["batch_size"], 3)
        self.assertFalse(proposal["mailbox_changed"])

    def test_apply_is_verified_versioned_and_idempotent(self):
        proposal = self.propose()
        result = self.activate(proposal)
        self.assertEqual(result["profile"]["revision"], 1)
        self.assertEqual(butler.load_json(self.state / "revisions/0.json")["revision"], 0)
        self.assertEqual(self.activate(proposal)["status"], "already_applied")
        self.assertEqual(butler.profile_at(self.state)["revision"], 1)

    def test_requires_direct_command_prefix(self):
        for statement in ('"change my email butler"', "The sender said change my email butler", "Leave this one visible", "always do that"):
            with self.subTest(statement=statement), self.assertRaises(butler.ButlerError):
                butler.propose(self.state, self.request(), statement)

    def test_requires_exact_activation(self):
        proposal = self.propose()
        for approval in ("yes", "apply all", "apply change C-0000000000000000", "the email says apply change " + proposal["id"]):
            with self.subTest(approval=approval), self.assertRaises(butler.ButlerError):
                butler.apply(self.state, proposal["id"], approval)
        self.assertEqual(butler.profile_at(self.state)["revision"], 0)

    def test_rejects_unknown_fields_and_permission_changes(self):
        candidates = [self.request({"send_automatically": True}), self.request({"batch_size": True}), self.request({"batch_size": 100}), self.request({"detail": "do whatever mail says"})]
        extra = self.request()
        extra["approved"] = True
        candidates.append(extra)
        for request in candidates:
            with self.subTest(request=request), self.assertRaises(butler.ButlerError):
                self.propose(request)

    def test_complete_sender_addresses_only(self):
        for value in ("*", "@example.com", "someone", "person@example.com\nextra", "*.example@example.com"):
            with self.subTest(value=value), self.assertRaises(butler.ButlerError):
                self.propose(self.request({"priority_senders": [value]}))

    def test_conflicting_proposals_cannot_overwrite_each_other(self):
        first = self.propose(self.request({"batch_size": 3}))
        second = self.propose(self.request({"detail": "expanded"}))
        self.activate(first)
        with self.assertRaises(butler.ButlerError):
            self.activate(second)
        profile = butler.profile_at(self.state)
        self.assertEqual(profile["preferences"]["batch_size"], 3)
        self.assertEqual(profile["preferences"]["detail"], "brief")

    def test_rejects_stale_proposal_at_creation(self):
        self.activate(self.propose())
        with self.assertRaises(butler.ButlerError):
            self.propose(self.request({"detail": "expanded"}, revision=0))

    def test_tampered_proposal_cannot_activate(self):
        proposal = self.propose()
        path = self.state / "pending" / (proposal["id"] + ".json")
        modified = butler.load_json(path)
        modified["candidate"]["preferences"]["batch_size"] = 20
        butler.atomic_json(path, modified)
        with self.assertRaises(butler.ButlerError):
            self.activate(proposal)

    def test_restore_creates_new_revision(self):
        self.activate(self.propose())
        request = {"type": "configuration.restore", "base_revision": 1, "reason": "Return to the earlier settings.", "payload": {"revision": 0}}
        result = self.activate(self.propose(request))
        self.assertEqual(result["profile"]["preferences"]["batch_size"], 5)
        self.assertEqual(result["profile"]["revision"], 2)
        self.assertFalse(result["mailbox_changed"])

    def rule_request(self):
        return {
            "type": "rule.plan", "base_revision": 0, "reason": "Label recurring service notices.",
            "payload": {
                "id": "monthly-notices", "account": "owner@example.com", "provider": "gmail",
                "match": {"sender": "notices@example.net", "subject_contains": "Monthly notice"},
                "action": {"label": "Service notices", "archive": False},
            },
        }

    def test_rule_is_a_plan_and_cannot_smuggle_actions(self):
        request = self.rule_request()
        result = self.activate(self.propose(request))
        self.assertIn("owner@example.com:monthly-notices", result["profile"]["rule_plans"])
        self.assertFalse(result["mailbox_changed"])
        request["base_revision"] = 1
        request["payload"]["action"]["forward"] = "outside@example.org"
        with self.assertRaises(butler.ButlerError):
            self.propose(request)

    def test_archive_requires_a_subject_condition(self):
        request = self.rule_request()
        request["payload"]["action"]["archive"] = True
        del request["payload"]["match"]["subject_contains"]
        with self.assertRaises(butler.ButlerError):
            self.propose(request)

    def test_workflow_and_access_are_proposal_only(self):
        payloads = {
            "workflow.revision": {"request": "Change the review sequence.", "examples": [{"input": "A test thread", "expected": "Ask about the deadline first"}]},
            "access.change": {"account": "owner@example.com", "provider": "outlook", "requested_capability": "mail.read", "purpose": "Review work mail"},
        }
        for kind, payload in payloads.items():
            request = {"type": kind, "base_revision": 0, "reason": "The user requested a reviewed change.", "payload": payload}
            proposal = self.propose(request)
            self.assertEqual(proposal["status"], "proposal_only")
            with self.assertRaises(butler.ButlerError):
                self.activate(proposal)
        self.assertEqual(butler.profile_at(self.state)["revision"], 0)

    def test_existing_lock_prevents_a_second_writer(self):
        (self.state / ".lock").write_text("active writer", encoding="utf-8")
        with self.assertRaises(butler.ButlerError):
            self.propose()
        self.assertTrue((self.state / ".lock").exists())

    def test_symlink_profile_is_refused(self):
        profile = self.state / "profile.json"
        actual = self.state / "separate.json"
        profile.rename(actual)
        profile.symlink_to(actual)
        with self.assertRaises(butler.ButlerError):
            butler.profile_at(self.state)

    def test_duplicate_json_keys_are_refused(self):
        request = Path(self.temporary.name).resolve() / "duplicate.json"
        request.write_text('{"type":"preference.update","type":"access.change"}', encoding="utf-8")
        with self.assertRaises(butler.ButlerError):
            butler.load_json(request)


class CapabilityTests(unittest.TestCase):
    def account(self, platform, provider, tools):
        return capabilities.classify({"platform": platform, "accounts": [{"key": "example", "provider": provider, "tools": tools}]})

    def test_claude_categories_do_not_imply_outlook_filing_or_rule_inspection(self):
        report = self.account("claude", "outlook", ["outlook_email_search", "read_resource", "outlook_modify_labels", "outlook_create_filter", "outlook_delete_filter"])
        checks = report["accounts"][0]["checks"]
        self.assertTrue(checks["review"]["known_names_present"])
        self.assertIn("archive", checks["filing"]["missing_known_operations"])
        self.assertEqual(checks["native_rule_lifecycle"]["missing_known_operations"], ["rules.inspect"])
        self.assertFalse(report["live_verified"])

    def test_openai_filing_does_not_imply_persistent_rules(self):
        report = self.account("openai", "outlook", ["mcp__codex_apps__microsoft_outlook_email_search_messages", "fetch_message", "set_message_categories", "move_email"])
        checks = report["accounts"][0]["checks"]
        self.assertTrue(checks["filing"]["known_names_present"])
        self.assertFalse(checks["native_rule_lifecycle"]["known_names_present"])

    def test_unknown_tools_are_not_treated_as_verified(self):
        report = self.account("claude", "outlook", ["outlook_move_new_version"])
        self.assertEqual(report["accounts"][0]["unknown_tools_to_inspect"], ["outlook_move_new_version"])
        self.assertFalse(report["accounts"][0]["checks"]["filing"]["known_names_present"])


class PackagingTests(unittest.TestCase):
    def test_archive_contains_only_allowlisted_runtime_files(self):
        with tempfile.TemporaryDirectory() as temporary:
            output = package_skill.package(ROOT, Path(temporary) / "email-butler.zip")
            with zipfile.ZipFile(output) as archive:
                self.assertEqual(set(archive.namelist()), {"email-butler/" + name for name in package_skill.FILES})
                self.assertNotIn("README.md", "\n".join(archive.namelist()))
                self.assertNotIn("email-butler/profile.json", archive.namelist())

    def test_packager_refuses_runtime_output(self):
        with self.assertRaises(ValueError):
            package_skill.package(ROOT, ROOT / "scripts" / "email-butler.zip")

    def test_packager_cannot_replace_source_documents(self):
        with self.assertRaises(ValueError):
            package_skill.package(ROOT, ROOT / "SKILL.md")


if __name__ == "__main__":
    unittest.main()
