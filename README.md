![Email Butler](assets/email-butler.png)

# Email Butler
An email assistant you operate through conversation. It helps you review Gmail and Outlook, organize recurring mail with native labels and rules, and change its behavior through a guarded review process.

This is an initial prototype distributed through its public Git repository. Your agent retrieves the code, installs the skill, and handles connector setup in the environment where you will use it. You do not need to create a Google Cloud project or install a separate service toolkit.

<h2><img src="assets/agent-hands-head-thumbs-up.png" height="32" alt="Robot head giving a thumbs-up"> Start here with your agent</h2>
Copy this prompt into your agent on the computer where you want to use Email Butler:

> Set up Email Butler from the public repository https://github.com/jcklpe/email-butler on this computer. Retrieve the repository, read AGENTS.md, SKILL.md, and references/setup.md, and handle the installation. Install or enable the official Gmail and Outlook/Microsoft 365 connectors for this agent, reusing any correct existing connections. Guide me through sign-in or permission clicks that require me. Check the actual accounts and capabilities available here, create private settings without overwriting existing ones, and show me a small email review using the defaults. Ask customization questions after I have something useful to react to. Keep private settings and mail out of Git. Do not ask me to use a terminal or edit code. If an actual restriction prevents a step, explain that specific restriction and what I need to do next.

The agent handles the technical steps. Your sign-in, consent, and required approvals stay with you. If a work-laptop or app restriction blocks setup, deal with that specific restriction when it occurs.

## Everyday use
- “Review my email.”
- “Show me what needs a decision.”
- “Help organize recurring messages.”
- “Change my email butler: make the reviews shorter.”

To change how it works from now on, start with **“change my email butler.”** It will explain what would change and ask you to confirm before saving it. Other feedback helps with the review you are doing now. You can also ask what changed before, or ask to go back to earlier settings.

Native mailbox rules handle predictable future messages after approval. The butler reviews exceptions and messages needing judgment. Creating a rule for future mail and cleaning up existing mail are separate actions.

## A manageable review
You get five emails at a time, with the most important decisions first. Each email has a short explanation, a link back to it when available, and a recommended action. You can approve individual items, change a recommendation, pause, or ask for the next batch. [Example review](references/review.md#chat-layout).

An overflowing inbox gets two tracks: keep up with new mail, then work through older mail in small sessions or clearly defined groups. The agent uses mailbox searches and native rules for repetitive cleanup instead of reading thousands of messages into a chat. Nothing is bulk archived just because it is old. [Backlog approach](references/organization.md#an-existing-backlog).

## Remembering and reducing the load
With private storage available, Email Butler remembers saved settings, review progress, confirmed mail actions, and clear feedback about recurring messages. You can ask “What do you remember?” or “What changed?” Personal history stays outside this public repository; you do not need to make commits.

Repeatedly archiving a newsletter can prompt “Keep receiving this, unsubscribe, or file it automatically?” The agent checks examples and exceptions with you before setting up a narrow filter or rule. It suggests unsubscribing from unwanted subscriptions and handles it through a supported connection when available, or shows the legitimate sender's unsubscribe link. It never treats silence as consent or changes your rules just because it noticed a pattern.

## Current limits
Setup verifies the recipient's actual agent, connectors, accounts, and permissions. Published documentation supplies pointers for that check; a successful or failed check on someone else's account does not establish readiness here. [Capability checks and documentation](references/capabilities.md).

Durable customization requires a private writable state location. The current helper supports local settings; shared settings across cloud chats and local agents still need a storage adapter. The agent must distinguish a saved change from a session-only adjustment.

## Package contents
The repository root is the skill: [SKILL.md](SKILL.md), [references](references/), [scripts](scripts/), and a synthetic default profile in [assets](assets/). All required workflow guidance and helper code ship together. There is no dependency on the author's personal workspace or Agent Hands installation. The setup marker reuses the Agent Hands robot artwork.

For maintainers, Python 3.11+ is sufficient; the runtime uses the standard library. Run `python3 -m unittest discover -s tests -v`. The bundled installer registers the Git checkout for supported local clients without copying the skill or overwriting an existing installation. Live connector onboarding and mailbox writes require acceptance testing in the recipient's environment; offline tests do not establish them.
