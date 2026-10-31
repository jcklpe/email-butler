#!/usr/bin/env python3
"""Register the Email Butler Git checkout for a selected local agent client."""

import argparse
import json
from pathlib import Path
import sys


class InstallError(ValueError):
    pass


CLIENT_DIRECTORIES = {
    "codex": Path(".agents") / "skills",
    "claude-code": Path(".claude") / "skills",
}
REQUIRED_FILES = (
    "SKILL.md", "references/setup.md", "references/changes.md",
    "references/organization.md", "references/capabilities.md",
    "assets/default-profile.json", "scripts/butler.py", "scripts/capabilities.py",
    "references/review.md", "references/memory.md", "scripts/journal.py", "scripts/review.py",
    "references/first-run.md",
    "references/conversation.md",
)


def install(source, client, skills_dir=None, execute=False):
    if client not in CLIENT_DIRECTORIES:
        raise InstallError("Unsupported client; inspect its supported installation mechanism")
    source = Path(source).resolve(strict=True)
    if not source.is_dir() or any(not (source / name).is_file() for name in REQUIRED_FILES):
        raise InstallError("The checkout is missing required Email Butler runtime files")
    base = Path(skills_dir) if skills_dir is not None else Path.home() / CLIENT_DIRECTORIES[client]
    target = base.absolute() / "email-butler"
    result = {
        "client": client, "source": str(source), "destination": str(target),
        "discovery_verified": False, "connectors_changed": False,
    }
    if target.exists() or target.is_symlink():
        if target.resolve() == source and target.is_dir():
            return {"status": "already_registered", **result}
        raise InstallError("An existing skill occupies the destination; it was left unchanged")
    if not execute:
        return {"status": "preview", **result}
    target.parent.mkdir(parents=True, exist_ok=True)
    try:
        target.symlink_to(source, target_is_directory=True)
    except FileExistsError:
        if target.is_symlink() and target.resolve() == source:
            return {"status": "already_registered", **result}
        raise InstallError("The destination changed during installation; it was left unchanged") from None
    except OSError as error:
        raise InstallError("The operating system blocked skill-link creation; use the client's supported installation path: " + str(error)) from None
    if not target.is_symlink() or target.resolve() != source or not (target / "SKILL.md").is_file():
        raise InstallError("Skill registration could not be verified; inspect the destination before retrying")
    return {"status": "registered", **result}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--client", required=True, choices=sorted(CLIENT_DIRECTORIES))
    parser.add_argument("--skills-dir", type=Path)
    parser.add_argument("--execute", action="store_true")
    args = parser.parse_args()
    try:
        result = install(Path(__file__).resolve().parent.parent, args.client, args.skills_dir, args.execute)
        print(json.dumps(result, indent=2))
        return 0
    except (InstallError, OSError) as error:
        print(json.dumps({"error": str(error), "connectors_changed": False}), file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
