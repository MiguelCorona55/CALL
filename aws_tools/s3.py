import logging
import pathlib

import boto3
from botocore.exceptions import ClientError

from settings import AUDIO_DIR_S3


def create_bucket(name, region=None):
    """Create an S3 bucket in a specified region"""

    # Create bucket
    try:
        if region is None:
            s3_client = boto3.client('s3')
            s3_client.create_bucket(Bucket=name)
        else:
            s3_client = boto3.client('s3', region_name=region)
            location = {'LocationConstraint': region}
            s3_client.create_bucket(Bucket=name,
                                    CreateBucketConfiguration=location)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def create_folders(folders, bucket):
    """Create one or more folders in a bucket"""

    try:
        s3_client = boto3.client('s3')
        for folder in folders:
            s3_client.put_object(Bucket=bucket, Key=folder)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def upload_file(file, bucket, name=None):
    """Upload a file to a bucket with an optional name"""

    if name is None:
        if isinstance(file, pathlib.PurePath):
            name = file.name
        else:
            name = pathlib.Path(file).name
    try:
        s3_client = boto3.client('s3')
        s3_client.upload_file(file, bucket, AUDIO_DIR_S3 + name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
