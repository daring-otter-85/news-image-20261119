#!/usr/bin/env python3
"""Deterministic entrypoint for the news-poster entry.

Copies the pre-rendered poster (entry.png, produced by
make_poster.py) byte-for-byte into the output folder named by
MAKEFUN_OUTPUT_DIR, falling back to /output when unset.
No network, no randomness, no re-rendering here.
"""

import os
import shutil
import sys


def main():
    here = os.path.dirname(os.path.abspath(__file__))
    source = os.path.join(here, "entry.png")
    if not os.path.isfile(source):
        print(f"missing poster image: {source}", file=sys.stderr)
        return 1
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR") or "/output"
    os.makedirs(out_dir, exist_ok=True)
    target = os.path.join(out_dir, "entry.png")
    shutil.copyfile(source, target)
    print(f"copied {source} -> {target}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
