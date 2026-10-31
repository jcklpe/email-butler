# Connector evidence
Checked 2026-10-31. These are dated findings, not a guarantee about an individual account or the next connector version. Inspect the host's actual tool schemas at setup. A signed-in Claude desktop session was inspected read-only, but its Microsoft 365 connector was not connected. No authenticated Microsoft 365 connector inventory or live mailbox write was available.

## Remaining Claude Outlook questions
| Capability | Evidence | Shipping posture |
| --- | --- | --- |
| Archive or move a message to an arbitrary mail folder | Absent from the published Microsoft 365 read/write tool tables; category changes are distinct from folder moves | Unverified; never advertise full filing support without an actual tool/schema and approved test |
| Create an inbox rule | outlook_create_filter is documented | Documented; account permission/schema/readback still required |
| Delete an inbox rule | outlook_delete_filter is documented | Documented; do not claim safe removal without exact ID and absence verification |
| List/get rules with criteria, actions, exceptions, and ordering | No rule-list/get tool documented; read_resource is described as reading files, emails, or chat by URI | Unverified; generic read_resource is not evidence of arbitrary Graph access |
| Categories | Creation, rename/delete, and message/thread/batch category changes are documented | Supported in principle; verify actual enabled tools and account |

The public directory and signed-in desktop connector detail page list the same seven read tools while the security guide documents additional writes. The desktop page showed a Connect action rather than an active Microsoft 365 connection; the inspection stopped before account connection or permission changes. This difference makes catalog omission alone insufficient proof of permanent absence. A credential-free POST tools/list to https://microsoft365.mcp.claude.com/mcp returned HTTP 401 on the check date. No new authentication was attempted and no mailbox content was accessed. Neither catalog inspection nor published documentation certifies an authenticated tenant's complete inventory.

**Conclusion:** a complete Claude-only butler, including Outlook filing and a safely inspectable native-rule lifecycle, is not established. Connector-based read/recommend/tag workflows remain useful. No custom OAuth service is implied by an incomplete connector.

## Other relevant capabilities
Claude's Gmail directory documents create_filter and list_filters, label creation/application/removal, and spam rescue. Its public list does not establish filter deletion. Gmail archive is removal of the INBOX system label, supported by the documented unlabel_thread schema. Some advanced Gmail filters are unsupported and attachment bodies are unavailable through Claude's Gmail connector.

The ChatGPT/Codex tools exposed in the development session support Gmail labels, archive, spam-label changes, paged searches and bulk labeling of existing matches; Outlook supports category management, folder discovery/creation, message moves, paged retrieval and attachments. That inventory exposes no Gmail-filter or Outlook-rule management tools. Exposed tools were inspected without reading account mail or performing a write. A future host may expose more.

## Sources
- [Anthropic Microsoft 365 security guide and full tool table](https://support.claude.com/en/articles/12684923-microsoft-365-connector-security-guide)
- [Anthropic Microsoft 365 directory](https://claude.com/marketplace/connectors/microsoft-365)
- [Connect Claude to Microsoft 365](https://support.claude.com/en/articles/15183774-connect-to-microsoft-365)
- [Anthropic Gmail directory](https://claude.com/marketplace/connectors/gmail)
- [Claude Google Workspace limitations](https://support.claude.com/en/articles/10166901-use-google-workspace-connectors)
- [Google Gmail MCP unlabel_thread schema](https://developers.google.com/workspace/gmail/api/reference/mcp/tools_list/unlabel_thread)
- [OpenAI inbox workflow](https://learn.chatgpt.com/use-cases/manage-your-inbox)

## Authenticated acceptance probe
In an authenticated Claude conversation, read this package and ask: “Inspect your actual Microsoft 365 connector tools and resource templates without changing mail. Can you move/archive a message, list/get inbox rules with their criteria/actions/ordering, create a rule, and delete a rule? Report exact exposed names and schema fields, with unavailable and unknown kept distinct. Do not call a write tool or invent a Graph URI. Distinguish exposed support from a successful read or write test.”

The inventory can settle exposed tool support. Identity checks and read-only rule inspection can settle read permission. An exact approved synthetic-message/rule cycle is still needed for write/readback verification. Do not create an uninspectable rule as a capability probe.
