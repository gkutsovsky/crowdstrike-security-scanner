import boto3
from botocore.exceptions import ClientError

# Utility function to start a Boto3 session with the specified profile and region

def start_aws_session(profile: str, region: str) -> boto3.Session:
    """Starts a general Boto3 session."""
    try:
        session = boto3.Session(
            profile_name=profile,
            region_name=region
        )
        return session
    except ClientError as e:
        print(f"Error starting AWS session: {e.response['Error']['Message']}")
    

