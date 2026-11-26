#!/usr/bin/env python3
"""news-image-20261126 entrypoint.

Takes the rendered poster sitting next to this script and places a copy
at the location the make.fun harness expects: $MAKEFUN_OUTPUT_DIR/entry.png.
When the harness variable is absent, fall back to an "output" folder
beside this file so the entry still runs standalone.
"""

import hashlib
import os
import shutil
from pathlib import Path


SOURCE_NAME = "poster.png"
TARGET_NAME = "entry.png"
FALLBACK_DIRNAME = "output"


def script_folder() -> Path:
    """Folder holding this script (and the poster next to it)."""
    return Path(__file__).resolve().parent


def destination_folder() -> Path:
    """Where entry.png should land.

    Prefer the harness-provided output directory; otherwise use a local
    "output" directory beside the script.
    """
    harness_dir = os.environ.get("MAKEFUN_OUTPUT_DIR")
    if harness_dir:
        return Path(harness_dir)
    return script_folder() / FALLBACK_DIRNAME


def copy_poster(source: Path, target: Path) -> None:
    """Copy the poster to the target path, creating folders as needed."""
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(source, target)


def digest_file(path: Path) -> str:
    """SHA-256 hex digest of a file, streamed in chunks."""
    hasher = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1 << 20), b""):
            hasher.update(chunk)
    return hasher.hexdigest()


def main() -> None:
    poster = script_folder() / SOURCE_NAME
    entry = destination_folder() / TARGET_NAME
    copy_poster(poster, entry)
    size = entry.stat().st_size
    digest = digest_file(entry)
    print(f"entry.png: {size} bytes")
    print(f"sha256: {digest}")


if __name__ == "__main__":
    main()
