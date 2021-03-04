import logging
import time

import boto3
from botocore.exceptions import ClientError

import settings
from aws_tools import iam, lmbd, cwe, s3

print('Starting setup...')

# This dict is for letting the user change the functions names without needing to change the zip files names when
# creating tha lambda functions
func_names = {
    'transcribe_audio': settings.TRANSCRIBE_FUNC_NAME,
    'parse_transcription': settings.PARSE_FUNC_NAME
}

try:

    # S3 setup
    s3_client = boto3.client('s3')
    bucket_waiter = s3_client.get_waiter('bucket_exists')
    object_waiter = s3_client.get_waiter('object_exists')

    s3.create_bucket(settings.AUDIO_BUCKET_NAME, settings.REGION)
    bucket_waiter.wait(Bucket=settings.AUDIO_BUCKET_NAME)
    s3.create_folders([settings.AUDIO_DIR_S3], settings.AUDIO_BUCKET_NAME)

    s3.create_bucket(settings.TRANSCRIPTIONS_BUCKET_NAME, settings.REGION)
    bucket_waiter.wait(Bucket=settings.TRANSCRIPTIONS_BUCKET_NAME)
    s3.create_folders([settings.TRANSCRIPTIONS_DIR], settings.TRANSCRIPTIONS_BUCKET_NAME)

    # object_waiter.wait(Bucket=settings.AUDIO_BUCKET_NAME, Key=settings.AUDIO_DIR_S3)
    # object_waiter.wait(Bucket=settings.TRANSCRIPTIONS_BUCKET_NAME, Key=settings.TRANSCRIPTIONS_DIR)
    # object_waiter.wait(Bucket=settings.CLASSIFICATION_BUCKET_NAME, Key=settings.AUDIO_DIR_S3)

    # IAM setup
    iam_client = boto3.client('iam')
    role_waiter = iam_client.get_waiter('role_exists')

    iam.create_role(settings.LAMBDA_ROLE_NAME, settings.ROLES_DIR / 'lambda_execute_role.json')
    role_waiter.wait(RoleName=settings.LAMBDA_ROLE_NAME)
    iam_client.attach_role_policy(PolicyArn='arn:aws:iam::aws:policy/AWSLambdaExecute',
                                  RoleName=settings.LAMBDA_ROLE_NAME)
    iam_client.attach_role_policy(PolicyArn='arn:aws:iam::aws:policy/AmazonTranscribeFullAccess',
                                  RoleName=settings.LAMBDA_ROLE_NAME)

    # Lambda
    lambda_client = boto3.client('lambda')
    time.sleep(10)

    for function_path in settings.LAMBDA_DIR.iterdir():
        func_name = func_names[function_path.stem]
        if func_name == settings.PARSE_FUNC_NAME:
            environ = {
                'TRANSCRIPTIONS_BUCKET_NAME': settings.TRANSCRIPTIONS_BUCKET_NAME,
                'TRANSCRIPTIONS_DIR': settings.TRANSCRIPTIONS_DIR
            }
        elif func_name == settings.TRANSCRIBE_FUNC_NAME:
            environ = {'LANGUAGE_CODE': settings.LANGUAGE_CODE}
        else:
            environ = None
        with open(function_path, 'rb') as code:
            role_arn = iam.get_role_arn(settings.LAMBDA_ROLE_NAME)
            lmbd.create_function(
                func_name,
                role_arn,
                code.read(),
                f'{function_path.stem}.lambda_handler',
                environ
            )

    function_waiter = lambda_client.get_waiter('function_exists')
    function_waiter.wait(FunctionName=settings.TRANSCRIBE_FUNC_NAME)

    lmbd.add_s3_trigger(
        settings.TRANSCRIBE_FUNC_NAME,
        settings.AUDIO_BUCKET_NAME,
        ['s3:ObjectCreated:*'],
        settings.TRANSCRIBE_FUNC_NAME + '_event',
        {
            'Key': {
                'FilterRules': [
                    {
                        'Name': 'prefix',
                        'Value': settings.AUDIO_DIR_S3
                    }
                ]
            }
        },
    )

    # CloudWatch
    function_waiter.wait(FunctionName=settings.PARSE_FUNC_NAME)
    cwe.create_rule_target_function(
        'parse',
        {
            "source": [
                "aws.transcribe"
            ],
            "detail-type": [
                "Transcribe Job State Change"
            ],
            "detail": {
                "TranscriptionJobStatus": [
                    "COMPLETED"
                ]
            }
        },
        settings.PARSE_FUNC_NAME,
        'Activates the parse_transcription function when a transcription job is completed'
    )


except ClientError as e:
    logging.error(e)

print('Setup completed!')
