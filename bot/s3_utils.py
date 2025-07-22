import boto3
import os
from dotenv import load_dotenv

load_dotenv()

s3 = boto3.client(
    's3',
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=os.getenv("AWS_REGION")
)

def upload_file(file_path: str, key: str) -> str:
    bucket = os.getenv("AWS_BUCKET_NAME")
    s3.upload_file(file_path, bucket, key)
    return f"https://{bucket}.s3.{os.getenv('AWS_REGION')}.amazonaws.com/{key}"

def generate_download_link(key: str, expires: int = 600) -> str:
    return s3.generate_presigned_url(
        ClientMethod='get_object',
        Params={
            'Bucket': os.getenv("AWS_BUCKET_NAME"),
            'Key': key
        },
        ExpiresIn=expires
    )