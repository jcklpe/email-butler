# Email Butler
An email assistant you operate through conversation. It helps you review Gmail and Outlook, organize recurring mail with native labels and rules, and change its behavior through a guarded review process.

This is an initial prototype. It uses existing account connectors; you do not need to create a Google Cloud project or install a separate service toolkit. The agent checks what your current app can actually do before promising actions.

## Start here
Give your agent access to this repository or an uploaded Email Butler skill package, then paste:

> Help me set up Email Butler from https://github.com/jcklpe/email-butler. Read SKILL.md and references/setup.md. Use my existing Gmail and Outlook connections where available. Handle the technical work and guide me through any necessary sign-in or approval clicks. Establish which accounts and actions this app supports, then show me a small email review using the defaults. Ask customization questions after I have something useful to react to. Keep private settings and mail out of the source repository. Do not ask me to use a terminal or edit files.

Connecting an account still requires your own sign-in and consent. If the agent cannot open the source or install a skill in your app, it should give you one concrete next step and accurately explain what remains unavailable.

## Everyday use
- “Review my email.”
- “Show me what needs a decision.”
- “Help organize recurring messages.”
- “Change my email butler: make the reviews shorter.”

The explicit phrase **“change my email butler”** opens a durable-change proposal. Ordinary corrections apply to the current review. The assistant shows the proposed change and waits for you to apply it. You can review prior changes and request a configuration rollback through the same process.

Native mailbox rules handle predictable future messages after approval. The butler reviews exceptions and messages needing judgment. Creating a rule for future mail and cleaning up existing mail are separate actions.

## Current limits
ChatGPT/Codex connectors expose routine Gmail and Outlook filing, but the tools reviewed for this prototype do not expose persistent filter/rule management. Claude documents Gmail filters and Outlook rule creation/deletion; Outlook archive/move and rule inspection are not established by its published tool list. Setup tests the actual tool inventory and reports a partial setup when necessary. [Capability evidence](references/capabilities.md).

Durable customization requires a private writable state location. A chat that cannot run the bundled validator or save state can still review email, but must say its adjustments are session-only. Uploaded skills and local skill copies do not automatically synchronize.

## Package contents
The repository root is the skill: [SKILL.md](SKILL.md), [references](references/), [scripts](scripts/), and a synthetic default profile in [assets](assets/). All required workflow guidance and helper code ship together. There is no dependency on the author's personal workspace or Agent Hands installation.

For maintainers, Python 3.11+ is sufficient; the runtime uses the standard library. Run `python3 -m unittest discover -s tests -v`. Build an uploadable ZIP with `python3 scripts/package_skill.py --output /chosen/path/email-butler.zip`. The packager includes only the runtime allowlist and refuses an output inside those runtime directories. Live connector onboarding and mailbox writes require separate acceptance testing; offline tests do not establish them.
