# Setup
The README prompt starts setup in the recipient's agent on their computer. The public Git repository carries the entire skill and its code. The agent handles retrieval, installation, connector setup, and verification. Read AGENTS.md and SKILL.md first. Do not add an archive upload route or make hypothetical work-laptop restrictions a setup questionnaire.

## First useful result
1. Retrieve https://github.com/jcklpe/email-butler into a suitable local folder using the agent's Git/file tools. Reuse an existing verified checkout without resetting user changes. Inspect the source before running its helpers. The repository root is the skill. If retrieval is actually blocked, report the exact restriction and the smallest user action needed; do not invent alternate distribution work in advance.
2. Identify the current client and its supported skill-discovery mechanism. For local Codex or Claude Code, the bundled scripts/install_skill.py previews a link from the client's skill directory to this checkout; use --execute within the user's requested installation scope. It preserves conflicting skills and creates no copied distribution. Detect Python or use the host's supported skill installer; the user never runs commands. If a different client exposes an installation API, use that API after checking its instructions. A local link is not proof of cloud-chat installation.
3. Inspect installed connections, then install/enable the official Gmail connector and the official Microsoft 365 connector in Claude or Outlook Email plugin in ChatGPT/Codex as needed. Use the host's own plugin/connector tools or supported setup interface. Reuse correct connections. Do not stop at saying a requested connector is missing when the host provides an install path. Do not copy connector credentials or configure an unverified third-party server. Bring the user in for their own sign-in, consent, account selection when ambiguous, and required approval clicks. Respect employer/admin restrictions rather than changing policy or expanding permissions to make setup pass.
4. Verify the recipient's selected identities and available tool schemas using authorized read-only checks. Distinguish installed, connected, permitted, and successfully tested. A developer's Claude/Codex configuration and static tool-name mappings do not establish any of these. Confirm skill discovery through the client's supported listing/reload mechanism when available; otherwise report discovery as unverified. Never claim setup is complete just because files or a plugin entry exist.
5. Establish a private state location without replacing an existing profile. With authorized account scope, read a small recent Inbox batch and show the default review. Use one short status covering the actual accounts and any meaningful gap. Ask preference questions after the preview. Do not mutate mail as a setup test.

## Local registration helper
For an agent with code execution, `python3 scripts/install_skill.py --client codex` or `--client claude-code` previews the destination. Add `--execute` to create the link within the requested installation scope. The documented defaults are the user's .agents/skills for Codex and .claude/skills for Claude Code. Inspect the actual client configuration first; --skills-dir selects a verified custom discovery directory. Never guess a client from the operating system alone or change discovery for other clients automatically.

An existing correct link is reused. A conflicting file, folder, or link is preserved and reported. If the operating system blocks link creation, handle that observed failure through the host's supported installation path; do not ask the user to run a terminal or silently overwrite the conflict. Source updates remain in the checkout; private personalization remains outside it. Verify discovery and connector access separately from filesystem registration.

## Capability probe
Inspect complete tool schemas and any read-only resource templates. Record their actual names and supported operations. Do not infer archive from a category tool, arbitrary Graph access from read_resource, rule inspection from a create response, or readback from delete returning success. Read references/capabilities.md for the unresolved Outlook checks.

The bundled scripts/capabilities.py accepts an inventory of observed tool names and reports known mappings and missing requirements. It is an offline inventory classifier, not a network tester. Unknown tools require schema inspection; missing known names do not prove a permanent platform limitation. Its output never certifies an operation as live-tested.

Inventory shape:
```json
{
  "platform": "claude",
  "accounts": [
    {"key": "work-outlook", "provider": "outlook", "tools": ["outlook_email_search", "read_resource", "outlook_create_filter", "outlook_delete_filter"]}
  ]
}
```

Run `python3 scripts/capabilities.py --inventory /private/path/inventory.json` only when the agent has code execution. A full capability check also inspects the schemas, verifies selected identities/permissions through authorized reads, and records actual readback behavior. Do not invent tool names to make the report pass.

## Private persistent state
Pick one private canonical location the chosen agents can actually read and write. Keep it outside the source repository and installed skill directory. A local agent may use a dedicated private directory. A cloud chat may use an explicitly selected private file in an existing connected storage service; that is additional storage access, not a feature of the mail connector itself. Keep account data within the chosen service's applicable boundaries. Do not use the public source repository or generalized conversational memory as the state store.

When code execution is available, initialize with `python3 scripts/butler.py init --state-dir /private/path/email-butler-state`. Python 3.11+ and its standard library are sufficient. Detect the runtime and resolve the chosen private directory to a canonical path first; managed state/input paths refuse symlinks. Do not make the user install Python or repair paths at a terminal. If the host lacks execution, the review can work without persistent customization.

For remote-file storage, the host must download the latest state with its revision/ETag, run the same validator in private scratch, conditionally save the new state, and independently read it back. Do not perform remote persistent changes when the storage route lacks a revision guard. Concurrent updates must not silently overwrite one another. The current helper implements local storage only; a remote synchronization adapter is not included or claimed tested. Report session-only customization until that adapter exists and is verified.

## Acceptance without surprise writes
Read-only setup cannot prove mailbox write success. Test a mailbox action only after showing an exact synthetic target and obtaining its specific approval. Check moving/archiving with a known test message and restore it only within the approved test scope. A test rule must have a unique name and a nonmatching exact condition; inspection, creation, deletion, and absence readback must each be supported and verified. If rule inspection is missing, do not create a rule merely to discover whether deletion works. Failure of a read never proves absence. An uncertain write is inspected before retrying.

Never silently fall back to browser automation or a new service integration. Offer supported partial triage plus one clear next step if full operation is unavailable.

## Host references
- [Codex local skill discovery and symlink support](https://learn.chatgpt.com/docs/build-skills)
- [Claude Code skill locations](https://code.claude.com/docs/en/skills)
- [Claude connector setup](https://support.claude.com/en/articles/11176164-use-connectors-to-extend-claude-s-capabilities)

Check current host instructions when a route differs from these documented defaults. Filesystem registration does not connect accounts, grant permissions, or certify runtime discovery.
