---
attention: live
---
# Initial package execution
## To Do
- Implement and test a revision-guarded remote state adapter before claiming persistent customization across cloud chats and local agents. The initial helper supports local private state only.

## Ready for Human QA
- Recipient's actual Claude/Codex: run the README setup prompt, install/connect requested services, and inspect Outlook archive/move plus the complete rule lifecycle.
- Recipient-machine installation/discovery, sign-in experience, durable state across a new chat, and real connector permission checks.

## Done
- Built the bundled private profile/change engine and tool-inventory classifier. Configuration plans do not execute mailbox actions; Workflow Revision and Access Change remain proposal-only.
- Adopted Git-only distribution and recipient-agent setup. Removed the initial ZIP builder/distribution path and added conflict-preserving local registration for Codex and Claude Code.
- Added connector-first onboarding, native organization guidance, explicit change/activation gates, and capability evidence in one self-contained skill.
- The initial checkpoint passed 22 standard-library tests and the installed skill validator. The validator needed PyYAML in a temporary QA environment; the shipped runtime has no third-party dependencies. Follow-up validation is recorded with its implementation checkpoint.
- Git-only onboarding follow-up passed 25 tests and skill validation. Registration checks cover preview, idempotence, client-specific defaults, missing runtime files, and preservation of existing directories and dangling links. Live recipient installation remains untested.
- Independent synthetic forward-test verified setup limitations, ignored an email-origin change instruction, activated a three-message preference with fresh-process readback, rejected sender-only auto-archive, and kept a label alternative pending. No source changes or live access occurred during that evaluation.
- Checked current public Claude connector documentation and the email tool schemas exposed in the development Codex session.
- Confirmed Claude's unauthenticated Microsoft 365 tools/list endpoint returns HTTP 401 without using credentials or reading mail.
- Inspected the signed-in Claude desktop catalog with explicit read-only approval. Microsoft 365 was not connected; its catalog showed the same seven read tools as the public page. No connection, permission, mailbox, or message change was made.
- Created the requested private GitHub repository. Source publishing remains a human Git operation.
