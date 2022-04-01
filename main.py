from typing import Optional
from fastapi import FastAPI
from pydantic import BaseModel
import os,shutil
# from keras.models import load_model
import pytorch_classification_script
from utils import downloadDirectoryFroms3, upload_to_aws, download_from_aws

app = FastAPI()

BUCKET_NAME = ""
currentPath = os.getcwd()


@app.get("/")
async def home():
    return "You have successfully landed!"

@app.get("/progress")
async def train_store(train_type : Optional[str] = None, bucket_name : Optional[str] = BUCKET_NAME): #Delete optional for bucket name later
    #Make necessary file operations
    
    bucketPath = os.path.join("train_data",bucket_name)
    if os.path.exists(os.path.join(currentPath,bucketPath)):
        shutil.rmtree(os.path.join(currentPath,bucketPath))
    os.mkdir(os.path.join(currentPath,bucketPath))

    #Importing data from cloud
    
    success = downloadDirectoryFroms3("training-server-client-"+ bucket_name[-1],"dataset",os.path.join(currentPath,"train_data",bucket_name))

    # success2 = download_from_aws("training-server-client-"+ bucket_name[-1],"annotations.json",os.path.join(currentPath,"train_data",bucket_name))
    if not(success):
            return {"download" : "fail"}
            
    #img = cv2.imread(currentPath+"/train_data/"+bucket_name+"/"+str(i))
    #print(img)         

    #Arrangement in weights directory

    weightsPath = os.path.join(currentPath,"weights",bucket_name)
    if os.path.exists(weightsPath):
        shutil.rmtree(weightsPath)
    os.mkdir(weightsPath)
                    
    #Initialize training                           
    if train_type == "classification":
        model = pytorch_classification_script.train(bucket_name)
        print(len(model))
        return {"Hi" : "Hi"}
        # model.save(os.path.join(weightsPath,"model.h5"))
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

    success = upload_to_aws(os.path.join(currentPath,"weights",bucket_name,"model.h5"),"training-server-model-"+bucket_name,"model.h5")
    if not success:
        return {"upload" : "fail"}
    
    del model

    return {
        "Training" : "Succesfull",
        "Storing" : "Succesfull"
    }

@app.get("/interrupt") #TODO
async def interrupt_training():
    pass
