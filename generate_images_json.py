"""Generate `images.json` listing all image files in the `images/` folder.

Run this script whenever you add/remove image files.

Usage:
  python generate_images_json.py
"""

import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
IMAGES_DIR = os.path.join(HERE, "images")
OUT_FILE = os.path.join(HERE, "images.json")

# File extensions to include (case-insensitive)
IMAGE_EXTS = {".png", ".jpg", ".jpeg", ".gif", ".webp", ".svg", ".bmp", ".tiff"}


def main() -> None:
    if not os.path.isdir(IMAGES_DIR):
        raise FileNotFoundError(f"Images directory not found: {IMAGES_DIR}")

    files = sorted(
        f
        for f in os.listdir(IMAGES_DIR)
        if os.path.isfile(os.path.join(IMAGES_DIR, f))
        and os.path.splitext(f)[1].lower() in IMAGE_EXTS
    )

    with open(OUT_FILE, "w", encoding="utf-8") as fp:
        json.dump(files, fp, indent=2)

    print(f"Wrote {len(files)} entries to {OUT_FILE}")


if __name__ == "__main__":
    main()
