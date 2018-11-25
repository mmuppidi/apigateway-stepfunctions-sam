
import boto3
import json
import os
import time

sfn_client = boto3.client('stepfunctions')


class APIEvent(object):

    def __init__(self, event):
        self.event = event

    @property
    def body(self):
        if self.event.get('body'):
            return json.loads(self.event['body'])
        return {}

    @property
    def path_parameters(self):
        if self.event.get('pathParameters'):
            return self.event['pathParameters']
        return {}

    @property
    def query_parameters(self):
        if self.event.get('queryStringParameters'):
            return self.event['queryStringParameters']
        return {}

    @property
    def resource_path(self):
        return self.event['resource']

    @property
    def http_method(self):
        return self.event['httpMethod'].upper()


def handler(event, context):
    event = APIEvent(event)

    response = sfn_client.start_execution(
        stateMachineArn=os.environ['STEP_FUNCTION_ARN'],
        input=json.dumps(event.body)
    )

    exec_arn = response['executionArn']

    status = sfn_client.describe_execution(executionArn=exec_arn)

    while status['status'] not in ('SUCCEEDED', 'FAILED', 'TIMED_OUT', 'ABORTED'):

        status = sfn_client.describe_execution(executionArn=exec_arn)
        time.sleep(1)

    return {
        'statusCode': 200,
        'body': json.dumps(status['output'])
    }
    
    