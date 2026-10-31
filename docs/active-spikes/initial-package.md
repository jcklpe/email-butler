---
attention: live
---
# Initial package
Create an agent-operated Gmail/Outlook assistant whose complete workflow, setup instructions, and helper code travel in one skill package. Existing connectors are the initial access route. No custom Google OAuth project, hosted mailbox bridge, or external toolkit is part of this scope.

## Adopted product requirements
Provide a useful initial preview before asking a long set of preference questions. Keep account coverage and meaningful limitations visible while handling technical details for the user. Use native labels, categories, and mailbox rules for predictable work. Require the direct-user phrase “change my email butler” to begin changes to durable behavior, with typed proposals, explicit activation, and rollback of local configuration.

## Initial implementation scope
Bundle Git-based recipient onboarding and local skill registration, a tool-inventory capability check, a strict private-profile writer, synthetic tests, and documentation pointers for recipient-side capability checks. Typed changes cover preferences, organization plans, rule plans, workflow revision requests, access change requests, and configuration restore. Workflow/access requests remain proposals until the separate implementation/authorization route is completed. Scripts do not call mail APIs or carry credentials.

## Distribution and setup
The public Git repository is the sole distribution route. The user copy-pastes the README prompt into their own agent, which retrieves the repository, installs the skill, installs/enables requested official connectors, and verifies that environment. Sign-in, consent, and required approvals stay with the user. Work-laptop restrictions are addressed when observed. No archive/upload path is maintained. Development-account inspection is not recipient acceptance evidence.

## Connector conclusion as of 2026-10-31
Claude's published Microsoft 365 tool table documents rule creation/deletion and category management but establishes neither archive/move nor rule listing/readback. Its directory listing is less complete than its security guide. These are research pointers for the recipient agent's setup checks. The earlier developer-account inspection and credential-free endpoint request did not establish recipient capabilities. The runtime discovers actual capabilities and handles observed limitations.

The maintained source is [references/capabilities.md](../../references/capabilities.md); it distinguishes published support, exposed tools, and live tests. Development records do not override that evidence or grant external access.

## State and verification
Keep user state outside source/distribution. Native rules remain canonical in the mailbox; a local rule plan does not prove installation. A script can validate structure and limits, but cannot authenticate the human origin of a CLI argument, judge whether a rule is wise, enforce the host's tools, or prevent an agent from bypassing files it can edit. Those limits must be explicit.

## Review, memory, and volume reduction
The chat review uses stable numbered blocks, defaults to five messages in total, and saves a private resumable queue. A queue records completion/deferral without carrying approvals into a new chat. Settings history is reconstructed from immutable proposals and saved profile revisions. A separate typed journal holds confirmed action receipts and clear feedback; it counts distinct messages and never edits policy. Local state survives fresh sessions using the same directory; shared cloud/local persistence still requires an adapter.

The organization workflow moves from reviewed patterns to one keep-receiving, unsubscribe, or narrow-native-rule discussion at a time. Archive counts alone do not establish unwanted mail. Large inboxes use recent-mail coverage plus bounded historical groups, native search/aggregation, and separately approved deterministic backfills. Inbox zero is a direction, not permission for an installation-time sweep or a claim that archived historical mail was read. The README includes the supplied logo and the shared Agent Hands start marker.

## Remaining acceptance work
Run the README prompt in the recipient's actual agent and capture exact schemas for archive/move, rule list/get/create/delete, and enabled account permissions. Test a known synthetic message and a uniquely named nonmatching rule only after their exact operations are approved. Verify durable state across a fresh chat and validate clean installation on that computer. Avoid claiming those checks from offline fixtures or another person's setup.
