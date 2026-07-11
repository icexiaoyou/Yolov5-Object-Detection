"""Validate the Ultralytics installation with one prediction."""
from __future__ import annotations
import argparse
from pathlib import Path
from ultralytics import YOLO

def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=Path("zidane.jpg"))
    parser.add_argument("--model", default="yolo11n.pt")
    args = parser.parse_args()
    results = YOLO(args.model).predict(source=str(args.source), verbose=False)
    print(f"Ultralytics is ready. Detections: {len(results[0].boxes)}")

if __name__ == "__main__":
    main()
