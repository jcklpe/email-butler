---
attention: live
---
# Initial package execution
## To Do
- Implement and test a revision-guarded remote state adapter before claiming persistent customization across cloud chats and local agents. The initial helper supports local private state only.

## Ready for Human QA
- Recipient's actual Claude/Codex: run the README setup prompt, install/connect requested services, and inspect Outlook archive/move plus the complete rule lifecycle.
- Recipient-machine installation/discovery, sign-in experience, durable state across a new chat, and real connector permission checks.
- Real review layout, pause/resume, pattern suggestions, unsubscribe route, and a bounded historical cleanup group in the recipient environment; no live mail or subscription test has been performed during development.

## Done
- Added conversational confirmation of one displayed change (yes / Apply this change) and short B-label selection among alternatives. Immutable IDs remain private. The helper refuses ambiguous selections, unseen/duplicate labels, stale profiles, and modified proposals. The 61-test suite and skill validation pass, including a fresh-process confirmation/readback check. An independent synthetic pass confirmed the single-preview Yes path, refused an ambiguous Yes among alternatives, and applied the selected short label with readback; no technical IDs appeared in its conversational transcript. Live recipient usability remains untested.
- Adopted 15-message text slates in the requested heading/link/arrow/unsubscribe/separator format, proactive rule checks, and guided first-run quick sorting. Stars/flags inform destinations and stay with filed mail; they do not create automatic Inbox exemptions. Direct user overrides remain authoritative, and Planner/document integrations stay outside this release.
- The first-run revision passes 56 standard-library tests and skill validation. Checks cover default sizing, preservation of existing preferences, retained marker/unsubscribe metadata, invalid link payloads, useful-mail filing candidates without automatic unsubscribe suggestions, and bounded typed folder/label plans. An independent synthetic pass produced the 15-message slate and guided group preview, retained markers without Inbox exemptions, honored a direct keep-in-Inbox override, and left native-rule creation unattempted when inspection/readback were unavailable. A focused independent follow-up activated/read back the folder scheme and narrow folder-rule plans locally, and refused broad or conflicting destinations without changing the profile. These are local plans, not mailbox installations. Live recipient cleanup remains untested.
- Review/memory follow-up passed 47 standard-library tests and skill validation. Fresh-process checks cover history, observation tallies, small review queues, deferrals, and state-location discovery. An independent synthetic forward test found one-off sizing, deferred-target visibility, and state-location gaps; focused regressions and an independent fresh-process follow-up confirm the implemented repairs. The follow-up preserved saved settings, retrieved deferred/uncertain targets, and located state without creating it before initialization. Live recipient behavior remains untested.
- Added the supplied logo and Agent Hands start marker; simplified the README's settings-change explanation.
- Defined the chat review layout, five-message combined slates, resumable private checkpoints, separate recent/backlog tracks, narrow native-rule promotion, and supported unsubscribe suggestions/actions.
- Added an applied-settings history view and a typed private observation journal with distinct-message tallies, honest operation statuses, and Outlook returned-identity deduplication. Observations do not mutate settings or authorize mailbox actions.
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
