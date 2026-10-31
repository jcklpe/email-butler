#!/usr/bin/env python3
"""Build an allowlisted Email Butler skill ZIP, excluding source-local user data."""

import argparse
import os
from pathlib import Path
import tempfile
import zipfile


FILES = (
    "SKILL.md", "assets/default-profile.json",
    "scripts/butler.py", "scripts/capabilities.py",
    "references/setup.md", "references/changes.md",
    "references/organization.md", "references/capabilities.md",
)


def package(root, output):
    root, output = Path(root).resolve(), Path(output).absolute()
    if output.suffix.lower() != ".zip":
        raise ValueError("Output must be a .zip file")
    if output.is_symlink():
        raise ValueError("Output cannot be a symlink")
    for directory in ("assets", "scripts", "references"):
        if output.resolve().is_relative_to((root / directory).resolve()):
            raise ValueError("Output must be outside runtime directories")
    for name in FILES:
        source = root / name
        if not source.is_file() or source.is_symlink() or source.resolve() != source.absolute():
            raise ValueError("Missing or symlinked runtime file: " + name)
    output.parent.mkdir(parents=True, exist_ok=True)
    fd, temporary = tempfile.mkstemp(prefix=".email-butler-", suffix=".zip", dir=output.parent)
    os.close(fd)
    try:
        with zipfile.ZipFile(temporary, "w", compression=zipfile.ZIP_DEFLATED) as archive:
            for name in FILES:
                archive.write(root / name, "email-butler/" + name)
        os.replace(temporary, output)
    finally:
        if os.path.exists(temporary):
            os.unlink(temporary)
    return output


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--output", required=True, type=Path)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent.parent
    result = package(root, args.output)
    print(result)


if __name__ == "__main__":
    main()
