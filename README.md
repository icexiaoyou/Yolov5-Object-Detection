@[TOC](Yolov5 Object Detection)
- [*1. Description*](#-1-description-)
  * [1.1. Yolov5 Offline Full Folder](#21-yolov5-offline-full-folder)
  * [1.2. WorkSpace Introduction](#22-workSpace-introduction)
- [*2. Preparation*](#-2-preparation-)
  * [2.1. Install Visual Studio Community 2022](#21-install-visual-studio-community-2022)
  * [2.2. Install Anaconda](#22-install-anaconda)
- [*3. Usage*](#-3-usage-)
- [*4. FlowChart*](#-4-flowchart-)


# *1. Description*

Object Detaction by **pytorch**, **yolov5** and **opencv**.
This project uses yolov5 to train a custom model. The project has the following functions.
## 1.1. Yolov5 Offline Full Folder
Thanks to my idol **ultralytics**, yolov5 makes AI more easier. This project is based on yolov5, here is Yolov5 officail github webside.
[https://github.com/ultralytics/yolov5](https://github.com/ultralytics/yolov5)
After download this repository, yolov5.pt have been download in 'yolov5' so you could use five different pre-tained model to generate a custom model offline.
## 1.2. WorkSpace Introduction
*The directory also includes two parts, which this project calls the workspace.*

The first part consists of three folders, named datasets, voc_dataset and yolo_dataset.<br>
datasets: the final storage location of the custom dataset<br>
voc_dataset: the storage location of pascal voc dataset<br>
yolo_dataset: the storage location of yolo dataset [temporary]

The second part consists of four scrpit, named test_installation.py, preprocess.py, voc_to_yolo.py and data_split.py. Full comments are in every python script.
# *2. Preparation*
## 2.1. Install Visual Studio Community 2022

Install the item named "C++ for Desktop Development".
## 2.2. Install Anaconda
```python
// Run Anaconda Prompt, coding...
conda create -n pytorch python>3.8
activate tensorflow
pip install pytorch
pip install labelImg
pip install opencv-python
pip install pillow
pip install shutil
pip install xml
pip install yaml
pip install json
pip install glob
```
# *3. Usage*
1. *[Optional*] Test the installation of yolov5 environment, please run "test_installation".
2. *[Optional*] Put images in folder named **"voc_dataset"**, subfolders named **"classes_index"**.	
3. Run **"preprocess.py"** to rename and resize the images.
4. Run **labelImg** to annotate all the images.
5. *[Optional*] Run **"voc_to_yolo.py"**, transform your dataset from pascal voc format to yolo format.
6. Run **"data_split.py"** to split yolo_dataset, generate train, valid and test dataset. In addition, you could enter "Y/N" to Confirm whether to generate final dataset and move to 'datasets'.
7. Follow **yolov5 officail guidence** to train and deploy your custom model.

 # *4. FlowChart*
 ![在这里插入图片描述](https://github.com/icexiaoyou/Yolov5-Object-Detection/blob/master/Yolov5-Object-detection.png)
