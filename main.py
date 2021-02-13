import logging

import boto3
from botocore.exceptions import ClientError

import settings
from aws_tools import s3, iam

try:

    # S3 setup
    s3_client = boto3.client('s3')
    bucket_waiter = s3_client.get_waiter('bucket_exists')
    object_waiter = s3_client.get_waiter('object_exists')

    s3.create_bucket(settings.BUCKET_NAME_AUDIO, settings.REGION)
    bucket_waiter.wait(Bucket=settings.BUCKET_NAME_AUDIO)
    s3.create_folders([settings.AUDIO_DIR_S3], settings.BUCKET_NAME_AUDIO)
    s3.create_bucket(settings.BUCKET_NAME_TRANSCRIPTIONS, settings.REGION)
    bucket_waiter.wait(Bucket=settings.BUCKET_NAME_TRANSCRIPTIONS)
    s3.create_folders([settings.TRANSCRIPTIONS_DIR], settings.BUCKET_NAME_TRANSCRIPTIONS)

    object_waiter.wait(Bucket=settings.BUCKET_NAME_AUDIO, Key=settings.AUDIO_DIR_S3)
    object_waiter.wait(Bucket=settings.BUCKET_NAME_TRANSCRIPTIONS, Key=settings.TRANSCRIPTIONS_DIR)

    # IAM setup
    iam_client = boto3.client('iam')
    role_waiter = iam_client.get_waiter('role_exists')

    iam.create_role('lambda-execute', settings.ROLES_DIR / 'lambda_execute_role.json')
    role_waiter.wait(RoleName='lambda-execute')
    iam.attach_policy('lambda-execute', 'arn:aws:iam::aws:policy/AWSLambdaExecute')

except ClientError as e:
    logging.error(e)

print('Setup completed!')
