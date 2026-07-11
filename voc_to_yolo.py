"""Convert Pascal VOC XML annotations to a flat YOLO detection dataset."""
from __future__ import annotations
import argparse
import shutil
import xml.etree.ElementTree as ET
from pathlib import Path
import yaml

IMAGE_EXTENSIONS = (".jpg", ".jpeg", ".png", ".bmp", ".webp")

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("voc_dataset"))
    parser.add_argument("--output", type=Path, default=Path("yolo_dataset"))
    parser.add_argument("--classes", required=True, help="Comma-separated class names in model order, for example: black,white")
    parser.add_argument("--overwrite", action="store_true")
    return parser.parse_args()

def find_image(xml_path: Path, filename: str | None) -> Path | None:
    candidates = [xml_path.parent / filename] if filename else []
    candidates.extend(xml_path.with_suffix(extension) for extension in IMAGE_EXTENSIONS)
    return next((path for path in candidates if path.exists()), None)

def main() -> None:
    args = parse_args()
    classes = [name.strip() for name in args.classes.split(",") if name.strip()]
    if not classes or len(set(classes)) != len(classes):
        raise SystemExit("--classes must contain unique, comma-separated class names.")
    if args.output.exists() and any(args.output.iterdir()) and not args.overwrite:
        raise SystemExit(f"Output directory is not empty: {args.output}. Use --overwrite to replace files.")
    images_dir, labels_dir = args.output / "images", args.output / "labels"
    images_dir.mkdir(parents=True, exist_ok=True)
    labels_dir.mkdir(parents=True, exist_ok=True)
    converted = 0
    for xml_path in sorted(args.source.rglob("*.xml")):
        root = ET.parse(xml_path).getroot()
        image = find_image(xml_path, root.findtext("filename"))
        if image is None:
            print(f"Skipping {xml_path}: image not found")
            continue
        size = root.find("size")
        width, height = int(size.findtext("width")), int(size.findtext("height"))
        relative_name = "_".join(xml_path.relative_to(args.source).with_suffix("").parts)
        target_image = images_dir / f"{relative_name}{image.suffix.lower()}"
        shutil.copy2(image, target_image)
        lines: list[str] = []
        for obj in root.findall("object"):
            name = obj.findtext("name", "").strip()
            if name not in classes:
                raise SystemExit(f"{xml_path}: unknown class {name!r}; expected one of {classes}")
            box = obj.find("bndbox")
            xmin, ymin = float(box.findtext("xmin")), float(box.findtext("ymin"))
            xmax, ymax = float(box.findtext("xmax")), float(box.findtext("ymax"))
            xmin, xmax = max(0, xmin), min(width, xmax)
            ymin, ymax = max(0, ymin), min(height, ymax)
            if xmax <= xmin or ymax <= ymin:
                print(f"Skipping invalid box in {xml_path}")
                continue
            lines.append(f"{classes.index(name)} {(xmin + xmax) / (2 * width):.6f} {(ymin + ymax) / (2 * height):.6f} {(xmax - xmin) / width:.6f} {(ymax - ymin) / height:.6f}")
        (labels_dir / f"{relative_name}.txt").write_text("\n".join(lines), encoding="utf-8")
        converted += 1
    (args.output / "data.yaml").write_text(yaml.safe_dump({"names": classes}, sort_keys=False), encoding="utf-8")
    print(f"Converted {converted} annotated images to {args.output}")

if __name__ == "__main__":
    main()
