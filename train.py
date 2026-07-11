"""Train a current Ultralytics YOLO detector on this repository's dataset."""
from __future__ import annotations
import argparse
from pathlib import Path
from ultralytics import YOLO

def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--data", type=Path, required=True, help="Path to data.yaml created by data_split.py")
    parser.add_argument("--model", default="yolo11n.pt", help="Ultralytics model checkpoint or model YAML")
    parser.add_argument("--epochs", type=int, default=100)
    parser.add_argument("--imgsz", type=int, default=640)
    parser.add_argument("--batch", type=int, default=-1, help="-1 selects an automatic batch size")
    parser.add_argument("--device", default=None, help="cpu, 0, 0,1, or leave unset for automatic selection")
    parser.add_argument("--project", type=Path, default=Path("runs"))
    return parser.parse_args()

def main() -> None:
    args = parse_args()
    model = YOLO(args.model)
    model.train(data=str(args.data), epochs=args.epochs, imgsz=args.imgsz, batch=args.batch,
                device=args.device, project=str(args.project), name="train", exist_ok=True)

if __name__ == "__main__":
    main()
