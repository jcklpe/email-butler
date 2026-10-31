# Email Butler
An email assistant you operate through conversation. It helps you review Gmail and Outlook, organize recurring mail with native labels and rules, and change its behavior through a guarded review process.

This is an initial prototype distributed through its public Git repository. Your agent retrieves the code, installs the skill, and handles connector setup in the environment where you will use it. You do not need to create a Google Cloud project or install a separate service toolkit.

## Start here
Copy this prompt into your agent on the computer where you want to use Email Butler:

> Set up Email Butler from the public repository https://github.com/jcklpe/email-butler on this computer. Retrieve the repository, read AGENTS.md, SKILL.md, and references/setup.md, and handle the installation. Install or enable the official Gmail and Outlook/Microsoft 365 connectors for this agent, reusing any correct existing connections. Guide me through sign-in or permission clicks that require me. Check the actual accounts and capabilities available here, create private settings without overwriting existing ones, and show me a small email review using the defaults. Ask customization questions after I have something useful to react to. Keep private settings and mail out of Git. Do not ask me to use a terminal or edit code. If an actual restriction prevents a step, explain that specific restriction and what I need to do next.

The agent handles the technical steps. Your sign-in, consent, and required approvals stay with you. If a work-laptop or app restriction blocks setup, deal with that specific restriction when it occurs.

## Everyday use
- “Review my email.”
- “Show me what needs a decision.”
- “Help organize recurring messages.”
- “Change my email butler: make the reviews shorter.”

The explicit phrase **“change my email butler”** opens a durable-change proposal. Ordinary corrections apply to the current review. The assistant shows the proposed change and waits for you to apply it. You can review prior changes and request a configuration rollback through the same process.

Native mailbox rules handle predictable future messages after approval. The butler reviews exceptions and messages needing judgment. Creating a rule for future mail and cleaning up existing mail are separate actions.

## Current limits
Setup verifies the recipient's actual agent, connectors, accounts, and permissions. Published documentation supplies pointers for that check; a successful or failed check on someone else's account does not establish readiness here. [Capability checks and documentation](references/capabilities.md).

Durable customization requires a private writable state location. The current helper supports local settings; shared settings across cloud chats and local agents still need a storage adapter. The agent must distinguish a saved change from a session-only adjustment.

## Package contents
The repository root is the skill: [SKILL.md](SKILL.md), [references](references/), [scripts](scripts/), and a synthetic default profile in [assets](assets/). All required workflow guidance and helper code ship together. There is no dependency on the author's personal workspace or Agent Hands installation.

For maintainers, Python 3.11+ is sufficient; the runtime uses the standard library. Run `python3 -m unittest discover -s tests -v`. The bundled installer registers the Git checkout for supported local clients without copying the skill or overwriting an existing installation. Live connector onboarding and mailbox writes require acceptance testing in the recipient's environment; offline tests do not establish them.
