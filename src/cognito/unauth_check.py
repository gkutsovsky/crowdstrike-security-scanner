import boto3
from botocore.exceptions import ClientError

# This function checks if unauthenticated access is enabled for a given Cognito Identity Pool and returns a dictionary with the check results

def check_unauthenticated_access(cognito_identity_client, identity_pool_id):
    try:
        response = cognito_identity_client.describe_identity_pool(
            IdentityPoolId=identity_pool_id
        )
        allow_unauthenticated_identities = response['AllowUnauthenticatedIdentities']
        if allow_unauthenticated_identities == True:
            status = 'FAIL'
        else:
            status = 'PASS'

        return {
            "check_id": "COGNITO_001",
            "title": "Unauthenticated Identity Pool Access Enabled",
            "status": status,
            "severity": "CRITICAL",
            "description": "Unauthenticated access is enabled for this identity pool, which can lead to unauthorized access to AWS resources.",
            "remediation": "Set to False to disable unauthenticated access",
            "affected_resources": [identity_pool_id]
        }

    except ClientError as e:
        error_message = e.response['Error']['Message']
        return {
            "check_id": "COGNITO_001",
            "title": "Unauthenticated Identity Pool Access Enabled",
            "status": 'ERROR',
            "severity": "CRITICAL",
            "description": f"Error checking unauthenticated access: {error_message}",
            "remediation": "Investigate the error and ensure the identity pool ID is correct.",
            "affected_resources": [identity_pool_id]
        }