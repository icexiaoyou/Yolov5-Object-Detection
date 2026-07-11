# YOLO Object Detection

This project modernizes the original YOLOv5 tutorial into a reproducible Ultralytics YOLO workflow. The repository name is preserved for existing links, but training now uses the actively maintained `ultralytics` package and its current YOLO models instead of the bundled legacy YOLOv5 checkout.

## Setup

PyTorch and TorchVision are managed by Conda. Ultralytics and the small application dependencies are installed with pip in that environment.

```powershell
conda env create -f environment.yml
conda activate yolov5-object-detection
python test_installation.py --source zidane.jpg
```

## Dataset workflow

Start with standard Pascal VOC XML annotations. Each XML must be beside its image; labels must exactly match the classes supplied on the command line.

```text
voc_dataset/
  black/
    black_001.jpg
    black_001.xml
  white/
    white_001.jpg
    white_001.xml
```

Convert and split the dataset deterministically:

```powershell
python voc_to_yolo.py --source voc_dataset --output yolo_dataset --classes black,white
python data_split.py --source yolo_dataset --output datasets/colors --classes black,white
```

The resulting `datasets/colors/data.yaml` contains absolute dataset metadata and is ready for Ultralytics.

## Train and predict

```powershell
python train.py --data datasets/colors/data.yaml --model yolo11n.pt --epochs 100 --imgsz 640
yolo detect predict model=runs/train/weights/best.pt source=path/to/image.jpg
```

`yolo11n.pt` is intentionally small for first runs. Change `--model` to a larger supported Ultralytics checkpoint when accuracy is more important than throughput.

The historical `yolov5/` directory remains only as an archived reference. New work should use the commands above.
