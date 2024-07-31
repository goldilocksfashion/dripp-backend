import boto3
from nuclio_sdk import Context
from datetime import datetime
import io, time
from app.event import Event
import pyarrow as pa
import pyarrow.parquet as pq
from typing import List

class S3Util:
    
    
    def __init__(self, context: Context, s3_client = None) -> None:
        self.aws_access_key_id=context.env['AWS_ACCESS_KEY_ID']
        self.aws_secret_access_key=context.env['AWS_SECRET_ACCESS_KEY']
        self.region_name=context.env['AWS_REGION']
        self.aws_bucket = context.env['AWS_BUCKET']
        if s3_client is None:
            self.client = boto3.client(
                's3',
                aws_access_key_id=self.aws_access_key_id,
                aws_secret_access_key=self.aws_secret_access_key,
                region_name=self.region_name
            )
        else:
            self.client = s3_client
        
        
    def  upload_to_s3(self, s3_key: str, buffer: io.BytesIO):
        """
        Uploads the buffer to S3, assumes parquet format ALWAYS
        """
        self.client.upload_fileobj(buffer, self.aws_bucket, s3_key)
        self.context.logger.info(f"Uploaded to s3://{self.aws_bucket}/{s3_key}")
