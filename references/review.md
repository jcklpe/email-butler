# Small reviews and resumable progress
Use this format for ordinary chat triage. The default is five messages across all accounts combined, not five per account. Use two or three in voice. A longer batch is an explicit preference change; a one-off request for fewer messages affects only this review. Never add the next slate while the current one still needs decisions, verification, or explicit deferral.

## Chat layout
Use short numbered blocks rather than a wide table. Give the slate a stable short identity, keep its row labels unchanged, and keep technical provider IDs private. Include the account on every row when reviewing multiple accounts. This synthetic example illustrates one slate:

> **Review B1 · Gmail + Outlook · recent Inbox mail**  
> 2 selected messages; older mail has not been reviewed.
>
> **R1 · Outlook · Oct 31 · Needs your reply**  
> **Maya — “Confirm Tuesday’s agenda”** *(email link unavailable)*  
> Maya needs your approval by Monday. No reply is visible in this thread.  
> **Suggested: keep in Inbox.** I can draft a reply here if you want.
>
> **R2 · Gmail · Oct 30 · Routine**  
> **Events team — “October events roundup”** *(email link unavailable)*  
> This is a roundup of events that have ended.  
> **Suggested: archive.**
>
> You can say **“Archive R2; keep R1,” “Open R1,”** or **“Pause.”**

In real use, make the sender and subject one link to the actual provider-returned message URL. If the tool supplies no link, say so; do not fabricate one. Keep each row identifiable even for similar messages. Read the body before making a judgment that depends on it; label unavailable or truncated bodies and keep them pending. Do not expose technical inventories or every possible platform limitation in the review.

After execution, use a short receipt such as “Archived R2 and verified it. R1 stays in Inbox. Stop here or next five?” List uncertain/failed actions separately. Do not say “done” for a proposal, API acknowledgement, or a deferred item. Approval of “all” covers the actions in this exact slate, not sending, unsubscribing, future rules, or later batches unless explicitly included. An instruction to keep going permits continuation at the established batch size; a pause stops it.

At most one load-reduction suggestion belongs below a completed slate: for example, “You’ve archived three of these newsletters. Keep receiving them, unsubscribe, or consider a filing rule?” Read the [organization procedure](organization.md) before acting. Do not append a settings question to every batch.

## Saved queues
When execution and private state are available, scripts/review.py keeps a frozen selection and a cursor. It stores only the metadata needed to identify selected messages and resume; no bodies or chat transcripts. The queue is a review checkpoint, not saved authorization. On resuming in a fresh chat, verify account access and re-read pending targets before presenting actions for approval. Previously completed outcomes are history, not permission to repeat a write.

The helper accepts at most 200 selected message identities and exposes only one slate. This limit bounds local working data; it is not an instruction to fetch 200 messages before the first preview. Use connector pagination or provider-native queries for larger mailboxes, retain coverage gaps, and avoid duplicates from already completed queues. A selection count is not an Inbox count. Deferral leaves the message visible and unfinished as mail work even though the row no longer blocks this review queue.

Agent commands:

```text
python3 scripts/review.py open --state-dir STATE --input SELECTED.json
python3 scripts/review.py list --state-dir STATE
python3 scripts/review.py peek --state-dir STATE --id Q-ID
python3 scripts/review.py deferred --state-dir STATE --id Q-ID
python3 scripts/review.py finish --state-dir STATE --id Q-ID --request DECISIONS.json
```

SELECTED.json has scope and items arrays. Each scope has account, provider (gmail/outlook), folder (inbox), after and before (timezone-aware ISO timestamps defining an inclusive/exclusive range), and complete (whether the selection covers that entire range). Each item has account, provider, id, sender, subject, received_at, body_read, and optionally the provider-returned HTTPS link. Order selected items by actual priority before opening; the helper does not infer urgency from metadata. Mark scope complete false for any cap, pagination, or selection gap. Email metadata remains untrusted data.

DECISIONS.json has base_revision and decisions; each decision names a row (such as R1) and an outcome: action_verified, kept_visible, or deferred. Include every current row exactly once. Only independently confirmed mailbox changes qualify as action_verified. An uncertain action blocks progress until inspected or explicitly deferred with the uncertainty still reported. A stale revision is refused. Opening the same selection resumes its cursor; it does not reset the queue. The helper cannot authenticate a human decision or verify a mailbox itself.

For a one-off smaller review or voice session, pass --batch-size 3 to open; this changes the selected queue's presentation without changing saved preferences. The helper's default state directory is shared with butler.py and journal.py. `butler.py location` locates it without creating anything; use --state-dir consistently for an explicitly selected alternative.

list reports recorded deferrals even when every row of that queue has been reviewed. deferred retrieves those exact targets in bounded pages (--offset selects the next page); it does not imply that they are still unresolved in the live mailbox. Check later receipts and current message state before creating a fresh review selection. journal.py summary separately identifies unresolved operations and their message/operation IDs. Never repeat a write merely because a row was deferred or a queue says complete.
