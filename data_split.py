import os
import shutil
import random
import yaml
import json


# ----------Custom Inputs for Scripts----------
# Set ratio
train_ratio = 0.8
val_ratio = 0.1
test_ratio = 0.1
# Folder which will be spilted
input_path = 'yolo_dataset'
output_path = 'yolo_splited_dataset'
# The name of your project(sanme as final name of dataset)
project = 'color_classify'
# Class names
class_names = ['b','w']
# Confirm whether to generate final dataset and move to 'datasets'
choice = input('Whether to automatically modify YAML and move Dataset to meet the requirements of train.py? Y/N: ')
# ----------That's ALL You Need to Do----------


# Initial output_path
if os.path.exists(output_path):
    shutil.rmtree(output_path)

# Generate the paths of input images and labels
input_images = os.path.join(input_path,'images')
input_labels = os.path.join(input_path,'labels')

# Get all paths of images 
image_files = os.listdir(os.path.join(input_path,'images'))

# Shuffle the order randomly
random.shuffle(image_files)

# Count file in three set
num_samples = len(image_files)
num_train = int(num_samples * train_ratio)
num_val = int(num_samples * val_ratio)
num_test = num_samples - num_train - num_val

# Create target folder
train_images = os.path.join(output_path,'train/images')
train_labels = os.path.join(output_path,'train/labels')
val_images = os.path.join(output_path,'val/images')
val_labels = os.path.join(output_path,'val/labels')
test_images = os.path.join(output_path,'test/images')
test_labels = os.path.join(output_path,'test/labels')

os.makedirs(train_images, exist_ok=True)
os.makedirs(train_labels, exist_ok=True)
os.makedirs(val_images, exist_ok=True)
os.makedirs(val_labels, exist_ok=True)
os.makedirs(test_images, exist_ok=True)
os.makedirs(test_labels, exist_ok=True)

# Delete all file in a folder
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

# Empty six new folder
delete_file(train_images)
delete_file(train_labels)
delete_file(val_images)
delete_file(val_labels)
delete_file(test_images)
delete_file(test_labels)

# Generate training set
for image_name in image_files[:num_train]:
    image_path = os.path.join(input_images, image_name)
    label_path = os.path.join(input_labels, image_name.replace(".jpg", ".txt"))
    shutil.copy(image_path, train_images)
    shutil.copy(label_path, train_labels)

# Generate validation set
for image_name in image_files[num_train:num_train+num_val]:
    image_path = os.path.join(input_images, image_name)
    label_path = os.path.join(input_labels, image_name.replace(".jpg", ".txt"))
    shutil.copy(image_path, val_images)
    shutil.copy(label_path, val_labels)

# Generate testing set
for image_name in image_files[num_train+num_val:]:
    image_path = os.path.join(input_images, image_name)
    label_path = os.path.join(input_labels, image_name.replace(".jpg", ".txt"))
    shutil.copy(image_path, test_images)
    shutil.copy(label_path, test_labels)

# Copy yaml
yaml_source = os.path.join(input_path,'data.yaml')
yaml_target = os.path.join(output_path,'data.yaml')
shutil.copy(yaml_source,yaml_target)

print('Dataset has splited!')


# Additional operation
if(choice=='Y'):
    # Copy entire folder and then remove the old
    target_path = os.path.join('datasets',project)
    if(os.path.exists(target_path)):
        shutil.rmtree(target_path)
    shutil.copytree(output_path,target_path)
    shutil.rmtree(output_path)
    # Create yaml in yolov5/data
    new_yaml = str(project + '.yaml')
    target_yaml = os.path.join('yolov5/data',new_yaml)
    json_string = json.dumps(class_names)
    with open(target_yaml, "w") as file:
        train_path = '../dataset/' + project + '/train/images'
        val_path = '../dataset/' + project + '/val/images'
        test_path = '../dataset/' + project + '/test/images'
        yaml.dump({'train': train_path}, file)
        yaml.dump({'val': val_path}, file)
        yaml.dump({'test': test_path}, file)
        file.write('\n')
        yaml.dump({'nc': len(class_names)}, file)
        file.write('names: ')
        file.write(str(json_string))
    print('You could use yolov5/train.py to train your custom dataset now!')
    print('Details: %s in datasets and %s in yolov5/data.' % (project,new_yaml))
    print('Enter yolov5 and run: python train.py --img 640 --batch 16 --epochs 3 --data ./data/%s --weights yolov5s.pt' % (new_yaml))
elif(choice == 'N'):
    print('Next, use train.py according to the official guidelines of yolov5.')


print('All Done!')