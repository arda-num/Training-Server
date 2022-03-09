from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import cv2
from secrets import access_key, secret_key
import boto3
from botocore.exceptions import NoCredentialsError
import os,shutil


app = FastAPI()

#Connecting S3 Service

ACCESS_KEY = access_key
SECRET_KEY = secret_key
BUCKET_NAME = "s3blob-anticode"
s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                      aws_secret_access_key=SECRET_KEY)


#S3 upload/download functions

def upload_to_aws(local_file, bucket, s3_file):
    global s3
    try:
        s3.upload_file(local_file, bucket, s3_file)
        return True
    except FileNotFoundError:
        return False
    except NoCredentialsError:
        return False

def download_from_aws(bucket_name,file_name,directory):
    global s3
    try:
        s3.download_file(bucket_name,file_name,directory)
        return True
    except:
        return False


@app.get("/")
async def home():
    return "You have successfully landed!"

@app.get("/progress")
async def train_store(image_count : int, train_type : Optional[str] = None, bucket_name : Optional[str] = BUCKET_NAME): #Delete optional for bucket name later
    #Make necessary file operations
    currentPath = os.getcwd()
    bucket_path = os.path.join("train_data",bucket_name)
    if os.path.exists(os.path.join(currentPath,bucket_path)):
        shutil.rmtree(os.path.join(currentPath,bucket_path))
    os.mkdir(os.path.join(currentPath,bucket_path))

    #Importing data from cloud
    for i in range(image_count):
        success = download_from_aws(bucket_name,str(i)+".png",currentPath+"/train_data/"+bucket_name+"/"+str(i)) #Assumed all image datas on the cloud is named as 0.png,1.png,2.png...
        if not(success):
            return {"download" : "fail"}

    #img = cv2.imread(currentPath+"/train_data/"+bucket_name+"/"+str(i))
    #print(img)         
                                        
    #Initialize training                           
    if train_type == "classification":
        #TODO
        pass
    elif train_type == "obj_detection":
        #TODO
        pass
    elif train_type == "instance_segmentation":
        #TODO
        pass
    else:
        #TODO
        return {"Train type" : "Undefined"} 

    #Store weights to cloud
    #TODO weights
    # for i in range(image_count):
    #     uploaded = upload_to_aws('local_file', bucket_name, 's3_file_name')
    #     if not(uploaded):
    #         return {"upload" : "fail"}
    return {
        "Training" : "Succesfull",
        "Storing" : "Succesfull"
    }

@app.get("/interrupt") #TODO
async def interrupt_training():
    pass

