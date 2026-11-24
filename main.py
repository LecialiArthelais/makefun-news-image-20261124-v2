#!/usr/bin/env python3
"""News-24 Round 3 entry (stdlib only).

Copies the committed entry.png sitting next to this script into the
grader's output directory. No third-party libraries, no fonts, no
rendering at run time -- the image is already rendered and committed
in the repo. The grader only needs plain Python to run this.
"""

import os
import shutil

HERE = os.path.dirname(os.path.abspath(__file__))
SRC = os.path.join(HERE, "entry.png")
OUT_DIR = os.environ.get("MAKEFUN_OUTPUT_DIR", ".")
DST = os.path.join(OUT_DIR, "entry.png")


def main():
    shutil.copyfile(SRC, DST)
    print("wrote " + DST)


if __name__ == "__main__":
    main()
