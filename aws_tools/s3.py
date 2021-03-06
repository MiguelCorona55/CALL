import pathlib

import boto3

from settings import AUDIO_DIR_S3


def create_bucket(name, region=None):
    """Create an S3 bucket in a specified region.

    Parameters
    ----------
    name : str
        Name of the bucket.
    region : str
        Code for the region. The default value is None.
    """
    if region is None:
        s3_client = boto3.client('s3')
        s3_client.create_bucket(Bucket=name)
    else:
        s3_client = boto3.client('s3', region_name=region)
        location = {'LocationConstraint': region}
        s3_client.create_bucket(Bucket=name,
                                CreateBucketConfiguration=location)


def create_folders(folders, bucket):
    """Create one or more folders in a bucket.

    Parameters
    ----------
    folders : list of str
        A list containing the names of the folders.
    bucket : str
        The name of the bucket in which the folders are going to be created.
    """
    s3_client = boto3.client('s3')
    for folder in folders:
        s3_client.put_object(Bucket=bucket, Key=folder)


def upload_file(fp, bucket, name=None):
    """Upload a file to a bucket with an optional name.
    
    Parameters
    ----------
    fp : str or pathlib.PurePath
        The file path.
    bucket : str
        Name of the bucket.
    name: str
        Name for the file once it is uploaded. The default value is None. If name is None,
        the file will be uploaded with it's original name.
    """

    if name is None:
        if isinstance(fp, pathlib.PurePath):
            name = fp.name
            fp = str(fp)
        else:
            name = pathlib.Path(fp).name

    s3_client = boto3.client('s3')
    s3_client.upload_file(fp, bucket, AUDIO_DIR_S3 + name)
