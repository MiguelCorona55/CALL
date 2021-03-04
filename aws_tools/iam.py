import json

import boto3


def create_policy(name, document):
    """Create a new policy from a json file.

    Parameters
    ----------
    name : str
        The policy name.
    document : path
        A path for the json file with instructions for creating a policy.
    """
    iam_client = boto3.client('iam')
    doc_json = json.load(document)
    iam_client.create_policy(PolicyName=name, PollicyDocument=json.dumps(doc_json))


def create_role(name, document):
    """Create a new role from a json file

    Parameters
    ----------
    name : str
        The role name.
    document : path
        A path for the json file with instructions for creating a role.
    """
    iam_client = boto3.client('iam')
    with open(document) as doc_json:
        role_document = json.load(doc_json)
    iam_client.create_role(RoleName=name, AssumeRolePolicyDocument=json.dumps(role_document))


def get_role_arn(role_name: str):
    """Return the role ARN."""
    iam_client = boto3.client('iam')
    return iam_client.get_role(RoleName=role_name)['Role']['Arn']
