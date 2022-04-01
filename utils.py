import os
import boto3
from secrets import access_key, secret_key
# from botocore.exceptions import NoCredentialsError


ACCESS_KEY = access_key
SECRET_KEY = secret_key



#S3 upload/download functions

def downloadDirectoryFroms3(bucket_name, s3_folder, local_dir=None):
    """
    Download the contents of a folder directory
    Args:
        bucket_name: the name of the s3 bucket
        s3_folder: the folder path in the s3 bucket
        local_dir: a relative or absolute directory path in the local file system
    """
    s3 = boto3.resource('s3',aws_access_key_id=ACCESS_KEY,
                            aws_secret_access_key=SECRET_KEY )
    bucket = s3.Bucket(bucket_name)
    for obj in bucket.objects.filter(Prefix=s3_folder):
        target = obj.key if local_dir is None \
            else os.path.join(local_dir, os.path.relpath(obj.key, s3_folder))
        if not os.path.exists(os.path.dirname(target)):
            os.makedirs(os.path.dirname(target))
        if obj.key[-1] == '/':
            continue
        try:
            bucket.download_file(obj.key, target)
        except:
            return False
    return True

def upload_to_aws(local_file, bucket, s3_file):
    try:
        s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                        aws_secret_access_key=SECRET_KEY)
        s3.upload_file(local_file, bucket, s3_file)
        return True
    except: 
        return False
    # except FileNotFoundError:
    #     return False
    # except NoCredentialsError:
    #     return False

def download_from_aws(bucket_name,file_name,directory):

    s3 = boto3.client('s3', aws_access_key_id=ACCESS_KEY,
                    aws_secret_access_key=SECRET_KEY)
    s3.download_file(bucket_name,file_name,directory)
