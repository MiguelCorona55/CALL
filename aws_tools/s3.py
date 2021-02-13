import logging
import pathlib

import boto3
from botocore.exceptions import ClientError

from settings import AUDIO_DIR_S3


def create_bucket(name, region=None):
    """Create an S3 bucket in a specified region.

    Parameters
    ----------
    name : str
        The name of the bucket.
    region : str
        The code for the region. The default value is None.
    """

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
    """Create one or more folders in a bucket.

    Parameters
    ----------
    folders : list of str
        A list containing the names of the folders.
    bucket : str
        The name of the bucket in which the folders are going to be created.
    """

    try:
        s3_client = boto3.client('s3')
        for folder in folders:
            s3_client.put_object(Bucket=bucket, Key=folder)
    except ClientError as e:
        logging.error(e)
        return False
    return True


def upload_file(fp, bucket, name=None):
    """Upload a file to a bucket with an optional name.
    
    Parameters
    ----------
    fp : str or pathlib.PurePath
        A string or an instance of pathlib.PurePath containing the path of the file.
    bucket : str
        The name of the bucket.
    name: str
        The name for the file once it is uploaded. The default value is None. If name is None, 
        the file will be uploaded with it's original name.
    """

    if name is None:
        if isinstance(fp, pathlib.PurePath):
            name = fp.name
        else:
            name = pathlib.Path(fp).name

    try:
        s3_client = boto3.client('s3')
        s3_client.upload_file(fp, bucket, AUDIO_DIR_S3 + name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
