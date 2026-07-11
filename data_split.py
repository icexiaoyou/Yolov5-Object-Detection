"""Create a deterministic YOLO train/validation/test split and dataset YAML."""
from __future__ import annotations
import argparse
import random
import shutil
from pathlib import Path
import yaml

IMAGE_EXTENSIONS = {".jpg", ".jpeg", ".png", ".bmp", ".webp"}

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("yolo_dataset"))
    parser.add_argument("--output", type=Path, default=Path("datasets/custom"))
    parser.add_argument("--classes", required=True, help="Comma-separated class names in model order")
    parser.add_argument("--train", type=float, default=0.8)
    parser.add_argument("--val", type=float, default=0.1)
    parser.add_argument("--seed", type=int, default=42)
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    if not 0 < args.train < 1 or not 0 < args.val < 1 or args.train + args.val >= 1:
        raise SystemExit("--train and --val must be positive and sum to less than 1.")
    classes = [name.strip() for name in args.classes.split(",") if name.strip()]
    images_dir, labels_dir = args.source / "images", args.source / "labels"
    images = sorted(path for path in images_dir.iterdir() if path.suffix.lower() in IMAGE_EXTENSIONS)
    if not images:
        raise SystemExit(f"No images found in {images_dir}")
    if args.output.exists() and any(args.output.iterdir()) and not args.overwrite:
        raise SystemExit(f"Output directory is not empty: {args.output}. Use --overwrite to replace files.")
    rng = random.Random(args.seed)
    rng.shuffle(images)
    train_end, val_end = int(len(images) * args.train), int(len(images) * (args.train + args.val))
    for split, items in (("train", images[:train_end]), ("val", images[train_end:val_end]), ("test", images[val_end:])):
        image_target, label_target = args.output / "images" / split, args.output / "labels" / split
        image_target.mkdir(parents=True, exist_ok=True)
        label_target.mkdir(parents=True, exist_ok=True)
        for image in items:
            shutil.copy2(image, image_target / image.name)
            label = labels_dir / f"{image.stem}.txt"
            if label.exists():
                shutil.copy2(label, label_target / label.name)
            else:
                (label_target / f"{image.stem}.txt").touch()
    config = {"path": str(args.output.resolve()), "train": "images/train", "val": "images/val", "test": "images/test", "names": classes}
    config_path = args.output / "data.yaml"
    config_path.write_text(yaml.safe_dump(config, sort_keys=False), encoding="utf-8")
    print(f"Wrote {len(images)} images and {config_path}")

if __name__ == "__main__":
    main()
