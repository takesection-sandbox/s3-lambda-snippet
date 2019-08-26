import json
import os.path
import boto3
import logging
import sys

LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)

def _loads(event):
    return event['Records']

def _load(record):
    event_time = record['eventTime']
    s3 = record['s3']
    bucket = s3['bucket']
    bucket_name = bucket['name']
    obj = s3['object']
    k = obj['key']
    s = obj['size']
    etag = obj['eTag']
    return {
        "eventTime": event_time,
        "bucketName": bucket_name,
        "key": k,
        "size": s,
        "eTag": etag
    }

def _process(record):
    info = _load(record)
    LOGGER.info("%s:%s" % (info['bucketName'], info['key']))

def lambda_handler(event, context):
    ex = False
    for record in _loads(event):
        try:
            _process(record)
        except:
            LOGGER.warn("error: %s", sys.exc_info()[0])
            ex = True
    if ex:
        raise

