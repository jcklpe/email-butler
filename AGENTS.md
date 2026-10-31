# Agent Instructions
Email Butler is one self-contained skill package. Keep its person-facing workflow, connector setup guidance, typed configuration code, and required references together. Do not introduce a dependency on a separate toolkit or the author's private workspace.

## Product boundaries
The user interacts with an agent, not a terminal or source editor. Prefer existing connectors. Never silently replace missing connector capabilities with browser automation, a new OAuth app, broader permissions, or a hosted service. Offer a concrete supported next step when a capability is missing.

Preserve the exact durable-change entry phrase, typed change classes, preview/activation separation, and honest persistence reporting in SKILL.md. A mailbox mutation is a separate operation from a local configuration change. Product permission boundaries cannot be changed through preference data.

## Development
Read README.md, SKILL.md, and the active spike linked from TODO.md. Use installed global Project Workflows procedures when available; they are development aids, not package dependencies. Active spike records live in docs/active-spikes/. Make local coherent checkpoints; never push or add co-author trailers. Keep private profiles, credentials, email exports, and test-account evidence out of Git and the skill ZIP. Use synthetic fixtures.

Run the standard-library test suite after changing scripts. Rebuild and inspect the package allowlist after changing distribution. Record connector claims as documented, exposed, live-verified, unavailable, or unknown; never promote documentation or a tool name to a successful mailbox test. Keep platform-specific evidence in references/capabilities.md and setup behavior in references/setup.md.
