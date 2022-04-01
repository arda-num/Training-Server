import os
import cv2
import json

def findExtension(filename):
    extension = ""
    for i in reversed(filename):
        if(i == "."):
            break
        extension += i
    extension_ret = ""
    for i in reversed(extension):
        extension_ret += i
    return extension_ret

def string_int_increment(string):
    zero_count = 0
    for i in string:
        if(i == '0'):
            zero_count += 1
        else:
            break
    if(zero_count == 8):
        number = 1
    else:
        number = int(string[zero_count:])
        number += 1
    new_string = str(number)
    for i in range(8-len(new_string)):
        new_string = "0"+new_string
    return new_string
    
def preprocess(directories):
    #TODO delete output
    os.system("mkdir output")

    annotations = dict()
    annotations["info"] = dict()
    annotations["licences"] = list()
    annotations["categories"] = list() #"id": 1, "name" : "cat", "supercategory" : "animal" 
    annotations["images"] = list() # "id" : 0, "licence" : 1, "file_name" : "0001.jpg", "height" : 324, "width" : 123, 
    annotations["annotations"] = list()  # "id" : 3, "image_id" : 0, "category_id" : 2, "bbox" : [11,22,33,44], "segmentation" : [...], "area" : 4353, "iscrowd" : 0

    counter = "00000000"
    id_img = 0
    id_category = 0
    id_annotation = 0
    currentPath = os.getcwd()
    for directory in directories:
        annotations["categories"].append({"id":id_category, "name":directory})
        id_category += 1
        for filename in os.listdir(directory):
            extension = findExtension(filename)
            img = cv2.imread(os.path.join(currentPath,directory,filename))
            # cv2.imshow("image",img)
            try:
                height = img.shape[0]
                width = img.shape[1]
                image_id = id_img
            except:
                continue
            annotations["images"].append({"id":image_id,"file_name":counter+"."+extension, "height":height, "width":width})
            annotations["annotations"].append({"id":id_annotation,"image_id":image_id, "category_id":id_category})
            f = os.path.join(currentPath,directory,filename)
            os.system("mv {} {}".format(os.path.join(currentPath,directory,filename),os.path.join(currentPath,"output",counter+"."+extension)))
            counter = string_int_increment(counter)
            id_img += 1 
            id_annotation += 1
            
    
    with open('annotations.json', 'w') as json_file:
        json.dump(annotations, json_file)

directories = ["Bishop", "King", "Knight", "Pawn", "Queen", "Rook"]
preprocess(directories)
cv2.waitKey(0)