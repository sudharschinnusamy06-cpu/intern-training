import boto3
import os
from fastapi import UploadFile

BUCKET_NAME = os.getenv("BUCKET_NAME")

s3_client = boto3.client("s3")

async def upload_file_to_s3(file: UploadFile, key: str) -> str:
    contents = await file.read()
    s3_client.put_object(
        Bucket=BUCKET_NAME,
        Key=key,
        Body=contents
    )
    url = f"https://{BUCKET_NAME}.s3.amazonaws.com/{key}"
    return url