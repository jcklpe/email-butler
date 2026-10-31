# Setup
The user should be able to hand this package to an agent and receive a useful review without installing a separate toolkit. Read SKILL.md first. Use the capabilities of the host actually running this conversation; a web chat cannot be assumed to access local files, invoke a local agent, or install skills automatically.

## First useful result
1. Inspect exposed connector tools without reading mail or changing settings. Resolve the selected Gmail/Outlook identity through a supported profile/account read. Ask which account only when selection is ambiguous. Never borrow the author's credentials or register a new OAuth app as a fallback.
2. Use one short status: “I can review Gmail and Outlook here; automatic Outlook rules are unavailable.” Distinguish exposed tools, successful authorized reads, missing tools, denied permissions, and unknowns. The package's dated platform report is orientation, not a replacement inventory.
3. With authorized account scope, read a small recent Inbox batch and show the default review. Ask preference questions after that preview. Do not mutate mail as a setup test.
4. For repeat use, install through the host's supported skill interface if available. The repository root is the skill. A local coding agent may use it directly or install a copy through its supported discovery mechanism. A chat host may require the user to upload the generated email-butler ZIP. Provide the required click instead of asking for terminal commands; do not claim installation from creating a file alone.

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
Pick one private canonical location the chosen agents can actually read and write. Keep it outside the source repository, installed skill directory, and distributable ZIP. A local agent may use a dedicated private directory. A cloud chat may use an explicitly selected private file in an existing connected storage service; that is additional storage access, not a feature of the mail connector itself. Keep account data within the chosen service's applicable boundaries. Do not use the public source repository or generalized conversational memory as the state store.

When code execution is available, initialize with `python3 scripts/butler.py init --state-dir /private/path/email-butler-state`. Python 3.11+ and its standard library are sufficient. Detect the runtime and resolve the chosen private directory to a canonical path first; managed state/input paths refuse symlinks. Do not make the user install Python or repair paths at a terminal. If the host lacks execution, the review can work without persistent customization.

For remote-file storage, the host must download the latest state with its revision/ETag, run the same validator in private scratch, conditionally save the new state, and independently read it back. Do not perform remote persistent changes when the storage route lacks a revision guard. Concurrent updates must not silently overwrite one another. The current helper implements local storage only; a remote synchronization adapter is not included or claimed tested. Report session-only customization until that adapter exists and is verified.

## Acceptance without surprise writes
Read-only setup cannot prove mailbox write success. Test a mailbox action only after showing an exact synthetic target and obtaining its specific approval. Check moving/archiving with a known test message and restore it only within the approved test scope. A test rule must have a unique name and a nonmatching exact condition; inspection, creation, deletion, and absence readback must each be supported and verified. If rule inspection is missing, do not create a rule merely to discover whether deletion works. Failure of a read never proves absence. An uncertain write is inspected before retrying.

Never silently fall back to browser automation or a new service integration. Offer supported partial triage plus one clear next step if full operation is unavailable.
