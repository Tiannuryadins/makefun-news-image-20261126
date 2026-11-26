#!/usr/bin/env python3
"""Entry point for make.fun bounty news-image-20261126.

Copies the pre-rendered 1024x1024 newspaper poster (poster.png, built
at authoring time by render_poster.py from news verified on 26 Nov
2026) to the make.fun output directory as entry.png.

Deterministic: the same poster.png bytes are copied on every run, so
two runs produce byte-identical entry.png files. No network access,
no randomness, no dependencies beyond the Python standard library.

Usage:
    MAKEFUN_OUTPUT_DIR=out python3 main.py   # writes out/entry.png
    python3 main.py                          # writes output/entry.png
"""

import hashlib
import os
import shutil
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCE = os.path.join(HERE, "poster.png")


def main() -> int:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "output")
    dest = os.path.join(out_dir, "entry.png")
    os.makedirs(out_dir, exist_ok=True)
    shutil.copyfile(SOURCE, dest)
    with open(dest, "rb") as fh:
        digest = hashlib.sha256(fh.read()).hexdigest()
    size = os.path.getsize(dest)
    print(f"wrote {dest} ({size} bytes, sha256 {digest})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
