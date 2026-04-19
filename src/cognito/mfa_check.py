import boto3 
from botocore.exceptions import ClientError

# This function takes in a Cognito client and a user pool ID, checks the MFA configuration for that user pool, and returns a dictionary with the check results

def check_mfa(cognito_client, user_pool_id):
    try:
        response = cognito_client.describe_user_pool(
            UserPoolId=user_pool_id
        )
        mfa_config = response['UserPool']['MfaConfiguration']
        
        if mfa_config in ['OFF', 'OPTIONAL']:
            status = 'FAIL'
        else:
            status = 'PASS'
            
        return {
            "check_id": "COGNITO_002",
            "title": "MFA Not Enforced",
            "status": status,
            "severity": "HIGH",
            "description": "MFA is not enforced",
            "remediation": "Set MfaConfiguration to ON",
            "affected_resources": [user_pool_id]
        }
        
    except ClientError as e:
        error_message = e.response['Error']['Message']
        return {
            "check_id": "COGNITO_001",
            "title": "MFA Not Enforced",
            "status": 'ERROR',
            "severity": "HIGH",
            "description": f"Error checking MFA configuration: {error_message}",
            "remediation": "Investigate the error and ensure the user pool ID is correct.",
            "affected_resources": [user_pool_id]
        }