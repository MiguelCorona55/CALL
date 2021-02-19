import boto3


def create_function(name, role, code, handler, environ=None):
    """Create a lambda function from a zip file.

    Parameters
    ----------
    name : str
        The name of the function.
    role : str
        The Amazon Resource Name (ARN) of the function's execution role.
    code : binary
        Binary data of the zip file containing the code.
    handler : str
         The name of the method within your code that Lambda calls to execute your function.
    environ : dict, optional
        A dictionary with environment variables.
    """
    if environ is None:
        environ = {}

    lambda_client = boto3.client('lambda')
    lambda_client.create_function(
        FunctionName=name,
        Runtime='python3.7',
        Role=role,
        Code={
            'ZipFile': code
        },
        Handler=handler,
        Environment={
            'Variables': environ
        }
    )


def get_func_arn(function_name: str):
    """Return the function ARN."""
    lambda_client = boto3.client('lambda')
    return lambda_client.get_function(FunctionName=function_name)['Configuration']['FunctionArn']


def add_s3_trigger(function_name, bucket_name, events, permission_id, filters=None):
    """Add a s3 trigger to the specified function.

    Parameters
    ----------
    function_name : str
        Name of the function to add the trigger.
    bucket_name : str
        Name of the bucket that triggers the Lambda function
    events : list of str
        Events in the bucket that trigger the  Lambda function.
    permission_id : str
        Id of the permission added to the bucket to invoke the function.
    filters : dict, optional
        Dictionary containing the prefixes and/or suffixes to filter the objects in the bucket by.
    """
    lambda_client = boto3.client('lambda')
    s3_client = boto3.client('s3')
    bucket_arn = 'arn:' + s3_client.meta.partition + ':s3:::' + bucket_name
    function_arn = get_func_arn(function_name)

    lambda_client.add_permission(
        FunctionName=function_name,
        StatementId=permission_id,
        Action='lambda:InvokeFunction',
        Principal='s3.amazonaws.com',
        SourceArn=bucket_arn
    )

    notification_configuration = {
        'LambdaFunctionConfigurations': [
            {
                'LambdaFunctionArn': function_arn,
                'Events': events,
            }
        ]
    }

    if filters is not None:
        notification_configuration['LambdaFunctionConfigurations'][0]['Filter'] = filters
    s3_client.put_bucket_notification_configuration(
        Bucket=bucket_name,
        NotificationConfiguration=notification_configuration
    )
