import logging
from typing import Optional
from botocore.exceptions import NoCredentialsError
import boto3
import os
import boto3
from botocore.exceptions import NoCredentialsError

class S3LogHandler(logging.Handler):
    """
    Custom logging handler to log messages to AWS S3 bucket.
    """
    def __init__(self, bucket, s3_key_prefix, aws_access_key_id=None, aws_secret_access_key=None):
        logging.Handler.__init__(self)
        self.bucket = bucket
        self.s3_key_prefix = s3_key_prefix
        if aws_access_key_id and aws_secret_access_key:
            self.s3_client = boto3.client('s3', aws_access_key_id=aws_access_key_id, aws_secret_access_key=aws_secret_access_key)
        else: 
            self.s3_client = boto3.client('s3')

    def emit(self, record):
        log_entry = self.format(record)
        s3_key = f"{self.s3_key_prefix}/{record.created}.log"
        try:
            self.s3_client.put_object(Bucket=self.bucket, Key=s3_key, Body=log_entry)
        except NoCredentialsError:
            print("AWS credentials not found.")
        except Exception as e:
            print(f"An error occurred: {e}")      


class LogUtil:
    """
    A utility class for logging messages to a file and an AWS S3 bucket.
    """
    def __init__(self, level : Optional[str] = None
                 , log_file: Optional[str] = 'app.log'):
        if os.environ.get('LOG_FILE') is not None:
            self.log_file = os.environ['LOG_FILE']
        else:
            self.log_file = log_file
            
        if os.environ.get('IS_DEBUG') is not None:
            print('Creating LogUtil instance.')
            self.level = 'DEBUG'
        elif level is None:
            self.level = 'ERROR'
        else:
            self.level = level

        self.log_file = log_file
        self.logger = logging.getLogger('LogUtil')
        self.logger.setLevel(self.level)
        self.handler = logging.FileHandler(self.log_file)
        self.formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        self.handler.setFormatter(self.formatter)
        self.logger.addHandler(self.handler)
        # Configure AWS S3 bucket details and credentials
        bucket_name = 'your-s3-bucket-name'
        s3_key_prefix = 'logs'
        aws_access_key_id = 'your-access-key'
        aws_secret_access_key = 'your-secret-key'
        s3_handler = S3LogHandler(bucket_name, s3_key_prefix, aws_access_key_id, aws_secret_access_key)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        s3_handler.setFormatter(formatter)
        self.logger.addHandler(s3_handler)
