import settings
import logging
import boto3
from botocore.exceptions import ClientError
from aws_tools import s3



try:
    s3_client = boto3.client('s3')
    bucket_waiter = s3_client.get_waiter('bucket_exists')
    object_waiter = s3_client.get_waiter('object_exists')

    s3.create_bucket(settings.BUCKET_NAME, settings.REGION)
    bucket_waiter.wait(Bucket=settings.BUCKET_NAME)
    s3.create_folders([settings.AUDIO_DIR, settings.TRANSCRIPTIONS_DIR], settings.BUCKET_NAME)
    object_waiter.wait(Bucket=settings.BUCKET_NAME, Key=settings.AUDIO_DIR)
    object_waiter.wait(Bucket=settings.BUCKET_NAME, Key=settings.TRANSCRIPTIONS_DIR)
except ClientError as e:
    logging.error(e)

print('Setup completed!')