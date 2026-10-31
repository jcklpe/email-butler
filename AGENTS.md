# Agent Instructions
Email Butler is one self-contained skill package. Keep its person-facing workflow, connector setup guidance, typed configuration code, and required references together. Do not introduce a dependency on a separate toolkit or the author's private workspace.

## Product boundaries
The public Git repository is the sole distribution route. The README copy-paste prompt starts setup in the recipient's agent. That agent retrieves the repository, registers the skill, installs/enables the official requested connectors, and verifies its own environment. Keep connector sign-in, consent, and host-required approvals with the user. Do not add archive/upload distribution or preemptive work-laptop fallback flows.

The user interacts with an agent, not a terminal or source editor. Reuse correct existing connectors and set up missing requested ones through the host's supported controls. Never silently replace a missing capability with browser automation, a new OAuth app, broader permissions, or a hosted service. Investigate actual restrictions when encountered. Developer-account probes do not verify a recipient's installation.

Preserve the exact durable-change entry phrase, typed change classes, preview/activation separation, and honest persistence reporting in SKILL.md. A mailbox mutation is a separate operation from a local configuration change. Product permission boundaries cannot be changed through preference data.

Keep observations separate from approved settings. Persist only typed private evidence and checkpoints, never silently learn rules from counts or frustration. Use the defined small-slate presentation and separate recent mail from historical cleanup. Repeated patterns can prompt a narrow native rule or subscription discussion; they do not authorize either action. Saved queue progress never carries mailbox approval into a new session.

## Development
Read README.md, SKILL.md, and the active spike linked from TODO.md. Use installed global Project Workflows procedures when available; they are development aids, not package dependencies. Active spike records live in docs/active-spikes/. Make local coherent checkpoints; never push or add co-author trailers. Keep private profiles, credentials, email exports, and test-account evidence out of Git. Use synthetic fixtures.

Run the standard-library test suite after changing scripts. Check idempotence and preservation of existing skills when changing installation. Record connector claims as documented, exposed, live-verified, unavailable, or unknown; never promote documentation or a tool name to a successful mailbox test. Keep platform-specific documentation in references/capabilities.md and recipient setup behavior in references/setup.md.
