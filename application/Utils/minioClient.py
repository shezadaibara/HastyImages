from minio.error import (ResponseError, BucketAlreadyOwnedByYou,
                         BucketAlreadyExists)
from minio import Minio
from django.conf import settings
import urllib3


class MC:
    """
    Singleton Class to handle MinioClient
    """
    __instance = None

    @staticmethod 
    def getInstance():
        """ Static access method. """
        if MC.__instance == None:
            MC()
        return MC.__instance

    def __init__(self):
        """ Virtually private constructor. """
        if MC.__instance != None:
            raise Exception("This class is a singleton!")
        else:
            self.client = Minio(
                settings.S3_CONFIG['MINIO_ENDPOINT'],
                access_key=settings.S3_CONFIG['AWS_UPLOAD_ACCESS_KEY_ID'],
                secret_key=settings.S3_CONFIG['AWS_UPLOAD_SECRET_KEY'],
                secure=settings.S3_CONFIG['SECURE'],
            )
            self.bucket = settings.S3_CONFIG['AWS_UPLOAD_BUCKET']
            self.region = settings.S3_CONFIG['AWS_UPLOAD_REGION']
            print("AWS_UPLOAD_BUCKET >> ", self.bucket)
            if not self.client.bucket_exists(self.bucket):
                try:
                    self.client.make_bucket(self.bucket, location=self.region )
                except BucketAlreadyOwnedByYou:
                    pass
                except BucketAlreadyExists:
                    pass
                except ResponseError:
                    raise
            MC.__instance = self
    
    

