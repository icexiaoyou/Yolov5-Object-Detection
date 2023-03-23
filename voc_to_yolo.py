# Transform pascal voc to yolo, file directory showed below the script.

import os
import os.path
import shutil
import yaml
import json
import xml.etree.ElementTree as ET
from glob import glob


# ----------Custom Inputs for Scripts----------
# Relative path of input_path & output_path
input_path = 'voc_dataset'
output_path = 'yolo_dataset'
# Class_num & Class_names
class_num = 2
class_names = ['b','w']
# ----------That's ALL You Need to Do----------


# Create and Initialize target folder
output_images = os.path.join(output_path,'images')
output_labels = os.path.join(output_path,'labels')
os.makedirs(output_images, exist_ok=True)
os.makedirs(output_labels, exist_ok=True)
def delete_file(folder_path):
    for filename in os.listdir(folder_path):
        file_path = os.path.join(folder_path, filename)
        try:
            if os.path.isfile(file_path) or os.path.islink(file_path):
                os.unlink(file_path)
            elif os.path.isdir(file_path):
                shutil.rmtree(file_path)
        except Exception as e:
            print(f"Failed to delete {file_path}. Reason: {e}")
delete_file(output_images)
delete_file(output_labels)

# Get subfolders and generate their absolute paths
def get_subs_abpath(path):
    list_abpath = []
    for root, dirs, files in os.walk(path):
        for directory in dirs:
            abpath = os.path.join(root, directory)
            list_abpath.append(abpath)
    return list_abpath

# Get all pictures from a folder, including .jpg/.png/.jpeg
def get_pics(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.jpg') or file_name.endswith('.png') or file_name.endswith('.jpeg'):
            pic = os.path.join(folder_path, file_name)
            pics.append(pic)
    return pics

# Get all xml from a folder
def get_xmls(folder_path):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.xml'):
            xml = os.path.join(folder_path, file_name)
            xmls.append(xml)
    return xmls

# Copy images or labels to target folder(images or labels)
def copy_file(list_file,folder_path):
    for file in list_file:
        shutil.copy(file,folder_path)

# Get absolute paths of all subfolders
subs_abpath = get_subs_abpath(input_path)

# Get absolute paths of all picture from all folder, store in pics
pics = []
for sub_abpath in subs_abpath:
    get_pics(sub_abpath)

# Get absolute paths of all xml from all folder, store in xmls
xmls = []
for sub_abpath in subs_abpath:
    get_xmls(sub_abpath)

# Copy all picture to images_path and all labels in labels
copy_file(pics,os.path.join(output_path,'images'))
copy_file(xmls,os.path.join(output_path,'labels'))

# Transform xml to txt
def xml_to_txt(xml_path,txt_path):
    files = []
    if not os.path.exists(txt_path):
        os.makedirs(txt_path)
    
    for root, dirs, files in os.walk(xml_path):
        None
    
    number = len(files)
    print(number)
    i = 0
    while i < number:
    
        name = files[i][0:-4]
        xml_name = name + ".xml"
        txt_name = name + ".txt"
        xml_file_name = os.path.join(xml_path,xml_name)
        txt_file_name = os.path.join(txt_path,txt_name)
    
        xml_file = open(xml_file_name)
        tree = ET.parse(xml_file)
        root = tree.getroot()
        # filename = root.find('name').text
    
        # image_name = root.find('filename').text
        w = int(root.find('size').find('width').text)
        h = int(root.find('size').find('height').text)
    
        f_txt = open(txt_file_name, 'w+')
        content = ""
    
        first = True
    
        for obj in root.iter('object'):
    
            name = obj.find('name').text
            class_num = class_names.index(name)
            # class_num = 0
    
            xmlbox = obj.find('bndbox')
    
            x1 = int(xmlbox.find('xmin').text)
            x2 = int(xmlbox.find('xmax').text)
            y1 = int(xmlbox.find('ymin').text)
            y2 = int(xmlbox.find('ymax').text)
    
            if first:
                content += str(class_num) + " " + \
                        str((x1 + x2) / 2 / w) + " " + str((y1 + y2) / 2 / h) + " " + \
                        str((x2 - x1) / w) + " " + str((y2 - y1) / h)
                first = False
            else:
                content += "\n" + \
                        str(class_num) + " " + \
                        str((x1 + x2) / 2 / w) + " " + str((y1 + y2) / 2 / h) + " " + \
                        str((x2 - x1) / w) + " " + str((y2 - y1) / h)
    
        # print(str(i / (number - 1) * 100) + "%\n")
        print(content)
        f_txt.write(content)
        f_txt.close()
        xml_file.close()
        i += 1

# XMLs transform to TXTs
xml_path = os.path.join(output_path,'labels')
txt_path = xml_path
xml_to_txt(xml_path,txt_path)

choice = input('Delete XMLs? Enter Y/N: ')
if(choice=='Y'):
    print('Delete all XMLs.')
    for xml in glob(os.path.join(xml_path,'*.xml')):
        os.remove(xml)
elif(choice=='N'):
    print('Keep all XMLs.')
else:
    print('Invalid, please enter Y or N.')

print("XMLs have transformed to TXTs!")

# Generate data.yaml
json_string = json.dumps(class_names)
path_yaml = os.path.join(output_path,'data.yaml')
with open(path_yaml, "w") as file:
    yaml.dump({'train': '../train/images'}, file)
    yaml.dump({'val': '../valid/images'}, file)
    yaml.dump({'test': '../test/images'}, file)
    file.write('\n')
    yaml.dump({'nc': class_num}, file)
    file.write('names: ')
    file.write(str(json_string))

print('PascalVOC has transform to Yolo!')
print('Detail: voc_dataset has copied and revise to yolo_dataset.')

# pascal voc dataset/
#     ├── class1/
#     │   ├── img1.jpg
#     │   ├── img2.jpg
#     │   ├── img1.xml
#     │   ├── img2.xml
#     ├── class2/
#     │   ├── img1.jpg
#     │   ├── img2.jpg
#     │   ├── img1.xml
#     │   ├── img2.xml

# yolo dataset/
#     ├── images
#     │   ├── img1.jpg
#     │   ├── img2.jpg
#     ├── labels
#     │   ├── img1.txt
#     │   ├── img2.txt
#     ├── data.yaml