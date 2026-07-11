"""Create a clean, resized Pascal VOC-style image dataset without changing originals."""
from __future__ import annotations
import argparse
from pathlib import Path
from PIL import Image, ImageOps

EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("voc_dataset"))
    parser.add_argument("--output", type=Path, default=Path("prepared_voc_dataset"))
    parser.add_argument("--image-size", type=int, default=640)
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    if not args.source.is_dir():
        raise SystemExit(f"Source directory does not exist: {args.source}")
    count = 0
    for image_path in sorted(path for path in args.source.rglob("*") if path.suffix.lower() in EXTENSIONS):
        target = args.output / image_path.relative_to(args.source).with_suffix(".jpg")
        target.parent.mkdir(parents=True, exist_ok=True)
        with Image.open(image_path) as image:
            image = ImageOps.exif_transpose(image).convert("RGB")
            image.thumbnail((args.image_size, args.image_size), Image.Resampling.LANCZOS)
            image.save(target, quality=95)
        xml_path = image_path.with_suffix(".xml")
        if xml_path.exists():
            raise SystemExit("Resizing annotated images changes bounding boxes. Run preprocessing before annotation, or use --source unchanged.")
        count += 1
    print(f"Wrote {count} images to {args.output}")

if __name__ == "__main__":
    main()
