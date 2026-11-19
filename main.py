#!/usr/bin/env python3
"""Entry point for news-image-20261119.

The repository holds one finished poster, entry.png, which sums up the
world news of Thursday, November 19, 2026.  This program copies that
image, byte for byte, to the output location the runner provides
(/output/entry.png, or $MAKEFUN_OUTPUT_DIR/entry.png when set).
No network, no randomness: two runs give identical bytes.
"""

import os
import shutil
from pathlib import Path

HERE = Path(__file__).resolve().parent
SOURCE = HERE / "entry.png"


def output_path() -> Path:
    out_dir = os.environ.get("MAKEFUN_OUTPUT_DIR", "/output")
    return Path(out_dir) / "entry.png"


def main() -> None:
    target = output_path()
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(SOURCE, target)
    print(f"wrote {target} ({target.stat().st_size} bytes)")


if __name__ == "__main__":
    main()
