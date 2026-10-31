---
attention: live
---
# Initial package
Create an agent-operated Gmail/Outlook assistant whose complete workflow, setup instructions, and helper code travel in one skill package. Existing connectors are the initial access route. No custom Google OAuth project, hosted mailbox bridge, or external toolkit is part of this scope.

## Adopted product requirements
Provide a useful initial preview before asking a long set of preference questions. Keep account coverage and meaningful limitations visible while handling technical details for the user. Use native labels, categories, and mailbox rules for predictable work. Require the direct-user phrase “change my email butler” to begin changes to durable behavior, with typed proposals, explicit activation, and rollback of local configuration.

## Initial implementation scope
Bundle connector-first onboarding, a tool-inventory capability check, a strict private-profile writer, synthetic tests, packaging, and an evidence-based capability report. Typed changes cover preferences, organization plans, rule plans, workflow revision requests, access change requests, and configuration restore. Workflow/access requests remain proposals until the separate implementation/authorization route is completed. Scripts do not call mail APIs or carry credentials.

## Connector conclusion as of 2026-10-31
Claude's published Microsoft 365 tool table documents rule creation/deletion and category management but establishes neither archive/move nor rule listing/readback. Its directory listing is less complete than its security guide. A read-only signed-in desktop catalog inspection confirmed the same seven read tools, but Microsoft 365 was not connected; no access expansion was attempted. An unauthenticated tools/list request returns 401. Therefore complete Claude-only operation is unverified. The runtime must discover actual capabilities and degrade explicitly.

The maintained source is [references/capabilities.md](../../references/capabilities.md); it distinguishes published support, exposed tools, and live tests. Development records do not override that evidence or grant external access.

## State and verification
Keep user state outside source/distribution. Native rules remain canonical in the mailbox; a local rule plan does not prove installation. A script can validate structure and limits, but cannot authenticate the human origin of a CLI argument, judge whether a rule is wise, enforce the host's tools, or prevent an agent from bypassing files it can edit. Those limits must be explicit.

## Remaining acceptance work
Run setup in an authenticated Claude session and capture exact schemas for archive/move, rule list/get/create/delete, and enabled account permissions. Test a known synthetic message and a uniquely named nonmatching rule only after their exact operations are approved. Verify durable state across a fresh chat and validate clean installation on the user's actual platform. Avoid claiming those checks from offline fixtures.
