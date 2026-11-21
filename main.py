#!/usr/bin/env python3
"""News image entry — 21 November 2026.

The image itself is rendered at build time and committed as output.png
next to this file. This program only places a copy of it where the
grader expects it: $MAKEFUN_OUTPUT_DIR/entry.png (or /output/entry.png).

Standard library only — nothing is installed before the program runs,
so this file imports nothing beyond the stdlib.
"""
import os
import shutil
import sys
from pathlib import Path


def entry_path() -> Path:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return Path(out_dir) / "entry.png"


def main() -> int:
    source = Path(__file__).resolve().parent / "output.png"
    if not source.is_file():
        print(f"missing image: {source}", file=sys.stderr)
        return 1
    dest = entry_path()
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, dest)
    size = dest.stat().st_size
    print(f"copied {source.name} -> {dest} ({size} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
