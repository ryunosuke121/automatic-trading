import boto3
from keras.models import load_model


s3_client = boto3.client('s3')

class LoadModelS3Service:
    def __init__(self, bucket_name):
        self.s3_bucket = s3_client.Bucket(bucket_name)

    def load_model(self, model_name, target_path):
        self.s3_bucket.download_file(model_name, target_path)
        return load_model(target_path)

class LoadModelService:
    def load_model(self, path: str):
        return load_model(path)