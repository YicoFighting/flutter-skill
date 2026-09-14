#!/usr/bin/env python3
"""Read-only validation of an explicitly selected Tuqiang checkout (Python 3.10+)."""

import argparse
import json
import re
import subprocess
import sys
from pathlib import Path


MARKERS = {
    "apps/standard/pubspec.yaml": "tuqiang_standard",
    "apps/ohos/pubspec.yaml": "tuqiang_ohos",
    "apps/tuqiang_app/pubspec.yaml": "tuqiang",
    "tool/project.dart": None,
}


def git(root: Path, *args: str) -> str:
    result = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True,
        text=True, encoding="utf-8", errors="strict", check=False,
    )
    if result.returncode:
        # Do not echo Git diagnostics that might contain private configuration.
        raise ValueError(f"Git {args[0]} failed (exit {result.returncode})")
    return result.stdout


def validate(candidate: Path) -> dict:
    candidate = candidate.expanduser().resolve(strict=True)
    directory = candidate.parent if candidate.is_file() else candidate
    root = Path(git(directory, "rev-parse", "--show-toplevel").strip()).resolve(strict=True)
    tracked = set(git(root, "ls-files", "-z", "--", *MARKERS).split("\0"))
    for relative, expected in MARKERS.items():
        path = root / relative
        if relative not in tracked or not path.is_file():
            raise ValueError(f"Missing tracked marker: {relative}")
        if not path.resolve().is_relative_to(root):
            raise ValueError(f"Marker escapes checkout: {relative}")
        content = path.read_text(encoding="utf-8")
        if content.startswith("\ufeff"):
            raise ValueError(f"UTF-8 BOM in marker: {relative}")
        if expected is not None:
            names = re.findall(
                r"^name:[ \t]*(['\"]?)([a-z][a-z0-9_]*)\1[ \t]*(?:#.*)?$",
                content, re.MULTILINE,
            )
            if len(names) != 1 or names[0][1] != expected:
                raise ValueError(f"Unexpected package identity: {relative}")
    return {
        "root": str(root),
        "product": "Tuqiang",
        "head": git(root, "rev-parse", "--verify", "HEAD").strip(),
        "markers": list(MARKERS),
    }


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", required=True, type=Path, help="Explicit checkout, directory or source file")
    args = parser.parse_args()
    try:
        print(json.dumps(validate(args.root), ensure_ascii=False, indent=2))
        return 0
    except (OSError, UnicodeError, ValueError) as error:
        print(f"Tuqiang root validation failed: {error}", file=sys.stderr)
        return 1


if __name__ == "__main__":
    raise SystemExit(main())
