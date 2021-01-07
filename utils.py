
import boto3
from botocore.config import Config

def get_session():
    return boto3.Session(aws_access_key_id="AKIA3FRGYDLIKFZC54VP", aws_secret_access_key= "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")

def get_polly_client():
    session = get_session()
    return session.client('polly', 'ca-central-1')

def get_rekonition_client():
    session = get_session()
    # config = Config(
    #     retries = dict(
    #         max_attempts = 10
    #     )
    # )
    # return session.client('rekognition',  'ca-central-1', config = config)
    return session.client('rekognition',  'us-east-2')

def get_s3_client():
    session = get_session()
    return session.client('s3', 'us-east-2')