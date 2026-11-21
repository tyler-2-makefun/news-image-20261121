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


PNG_MAGIC = b"\x89PNG\r\n\x1a\n"


def verify_copy(source: Path, dest: Path) -> str | None:
    """Check the copied file is a faithful copy of the source image.

    Returns an error message when something is wrong, else None.
    A silent partial or corrupted copy would make the grader score a
    broken image (or fail to find one), so the program refuses to
    report success unless the output exists, has exactly the source
    size, and starts with a valid PNG header.
    """
    if not dest.is_file():
        return f"output missing after copy: {dest}"
    expected = source.stat().st_size
    actual = dest.stat().st_size
    if actual != expected:
        return (
            f"size mismatch: {dest} is {actual} bytes, "
            f"expected {expected} bytes from {source.name}"
        )
    with dest.open("rb") as f:
        header = f.read(len(PNG_MAGIC))
    if header != PNG_MAGIC:
        return f"bad PNG header in {dest}: {header!r}"
    return None


def main() -> int:
    source = Path(__file__).resolve().parent / "output.png"
    if not source.is_file():
        print(f"missing image: {source}", file=sys.stderr)
        return 1
    dest = entry_path()
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, dest)
    error = verify_copy(source, dest)
    if error is not None:
        print(f"copy verification failed: {error}", file=sys.stderr)
        return 1
    size = dest.stat().st_size
    print(f"copied {source.name} -> {dest} ({size} bytes, verified PNG)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
