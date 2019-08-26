import sys
import boto3
import json
import logging
import urllib.request

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

def lambda_handler(event, context):
    LOGGER.info("event: %s", event)

    response_url = event['ResponseURL']

    stack_id = event['StackId']
    request_id = event['RequestId']
    logical_resource_id = event['LogicalResourceId']

    log_stream_name = context.log_stream_name

    bucket_name = event['ResourceProperties']['BucketName']
    LOGGER.info("BucketName: %s", bucket_name)

    lambda_configurations = event['ResourceProperties']['LambdaFunctionConfigurations']
    LOGGER.info("LambdaFunctionConfigurations: %s", lambda_configurations)

    client = boto3.client('s3')

    try:
        if event['RequestType'] == "Create":
            client.put_bucket_notification_configuration(
                Bucket = bucket_name,
                NotificationConfiguration = {
                    'LambdaFunctionConfigurations': lambda_configurations
                }
            )
            put_response(response_url, {
                "Status": "SUCCESS",
                "Reason": "See the details in CloudWatch Log Stream: %s" % log_stream_name,
                "StackId": stack_id,
                "RequestId": request_id,
                "LogicalResourceId": logical_resource_id,
                "PhysicalResourceId": "%s-%s" % (stack_id, logical_resource_id)
            })
        elif event['RequestType'] == "Update":
            client.put_bucket_notification_configuration(
                Bucket = bucket_name,
                NotificationConfiguration = {
                    'LambdaFunctionConfigurations': lambda_configurations
                }
            )
            put_response(response_url, {
                "Status": "SUCCESS",
                "Reason": "See the details in CloudWatch Log Stream: %s" % log_stream_name,
                "StackId": stack_id,
                "RequestId": request_id,
                "LogicalResourceId": logical_resource_id,
                "PhysicalResourceId": "%s-%s" % (stack_id, logical_resource_id)
            })
        elif event['RequestType'] == "Delete":
            client.put_bucket_notification_configuration(
                Bucket = bucket_name,
                NotificationConfiguration = {}
            )
            put_response(response_url, {
                "Status": "SUCCESS",
                "Reason": "See the details in CloudWatch Log Stream: %s" % log_stream_name,
                "StackId": stack_id,
                "RequestId": request_id,
                "LogicalResourceId": logical_resource_id,
                "PhysicalResourceId": "%s-%s" % (stack_id, logical_resource_id)
            })
        else:
            put_response(response_url, {
                "Status": "FAILED",
                "Reason": "See the details in CloudWatch Log Stream: %s" % log_stream_name,
                "StackId": stack_id,
                "RequestId": request_id,
                "LogicalResourceId": logical_resource_id,
                "PhysicalResourceId": "%s-%s" % (stack_id, logical_resource_id)
            })
    except:
        LOGGER.warn("error: %s", sys.exc_info()[0])
        put_response(response_url, {
            "Status": "FAILED",
            "Reason": "See the details in CloudWatch Log Stream: %s" % log_stream_name,
            "StackId": stack_id,
            "RequestId": request_id,
            "LogicalResourceId": logical_resource_id,
            "PhysicalResourceId": "%s-%s" % (stack_id, logical_resource_id)
        })

def put_response(url, res):
    entity = json.dumps(res)
    LOGGER.info("json: %s", entity)
    headers = {
        'Content-Type': 'application/json',
        'Content-Length': len(entity)
    }
    req = urllib.request.Request(url, entity.encode(), headers, method = 'PUT')
    with urllib.request.urlopen(req) as put_res:
        LOGGER.info("Status code: %s", put_res.getcode())
        LOGGER.info("Status message: %s", put_res.msg)
