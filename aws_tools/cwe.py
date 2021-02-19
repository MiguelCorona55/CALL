import json

import boto3

from aws_tools.lmbd import get_func_arn


def create_rule_target_function(rule_name, event_pattern, function_name, rule_description=''):
    """Create a CloudWatch rule for the specified function.

    Parameters
    ----------
    rule_name : str
        Name for the rule.
    event_pattern : dict
        Dictionary with the information of the event pattern.
    function_name : str
        Name of the target function.
    rule_description : str, optional
        Description of the CloudWatch rule.
    """
    cwe_client = boto3.client('events')
    lambda_client = boto3.client('lambda')
    rule_arn = cwe_client.put_rule(
        Name=rule_name,
        EventPattern=json.dumps(event_pattern),
        Description=rule_description
    )
    lambda_client.add_permission(
        FunctionName=function_name,
        StatementId=function_name + '_event',
        Action='lambda:InvokeFunction',
        Principal='events.amazonaws.com',
        SourceArn=rule_arn['RuleArn']
    )
    cwe_client.put_targets(
        Rule='parse',
        Targets=[
            {
                'Id': 'target_' + function_name,
                'Arn': get_func_arn(function_name)
            }
        ]
    )
