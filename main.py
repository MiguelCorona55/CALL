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

    s3.create_bucket(settings.BUCKET_NAME, settings.REGION)
    bucket_waiter.wait(Bucket=settings.BUCKET_NAME)
    s3.create_folders([settings.AUDIO_DIR_S3, settings.TRANSCRIPTIONS_DIR], settings.BUCKET_NAME)
    object_waiter.wait(Bucket=settings.BUCKET_NAME, Key=settings.AUDIO_DIR_S3)
    object_waiter.wait(Bucket=settings.BUCKET_NAME, Key=settings.TRANSCRIPTIONS_DIR)

    # IAM setup
    iam_client = boto3.client('iam')
    role_waiter = iam_client.get_waiter('role_exists')

    iam.create_role('lambda-execute', settings.ROLES_DIR / 'lambda_execute_role.json')
    role_waiter.wait(RoleName='lambda-execute')
    iam.attach_policy('lambda-execute', 'arn:aws:iam::aws:policy/AWSLambdaExecute')

except ClientError as e:
    logging.error(e)

print('Setup completed!')
