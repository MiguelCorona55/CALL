import json
import logging

import boto3
from botocore.exceptions import ClientError


def create_policy(name, document):
    """Create a new policy from a json file.

    Parameters
    ----------
    name : str
        The policy name.
    document : path
        A path for the json file with instructions for creating a policy.
    """
    try:
        iam_client = boto3.client('iam')
        doc_json = json.load(document)
        iam_client.create_policy(PolicyName=name, PollicyDocument=json.dumps(doc_json))
    except ClientError as e:
        logging.error(e)
        return False
    return True


def create_role(name, document):
    """Create a new role based on a json file

    Parameters
    ----------
    name : str
        The role name.
    document : path
        A path for the json file with instructions for creating a role.
    """
    try:
        iam_client = boto3.client('iam')
        with open(document) as doc_json:
            role_document = json.load(doc_json)
        iam_client.create_role(RoleName=name, AssumeRolePolicyDocument=json.dumps(role_document))
    except ClientError as e:
        logging.error(e)
        return False
    return True


def attach_policy(role_name, policy_arn):
    """Attach an existent policy to an existent role.

    Parameters
    ----------
    role_name : str
        The role name.
    policy_arn : str
        A string representing the ARN of the policy.
    """
    try:
        iam_client = boto3.client('iam')
        iam_client.attach_role_policy(PolicyArn=policy_arn, RoleName=role_name)
    except ClientError as e:
        logging.error(e)
        return False
    return True
