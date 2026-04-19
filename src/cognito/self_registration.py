import boto3
from botocore.exceptions import ClientError

# This function checks if self registration is enabled for a given Cognito User Pool and returns a dictionary with the check results
def check_self_registration(cognito_client, user_pool_id):
    try:
        response = cognito_client.describe_user_pool(
            UserPoolId=user_pool_id
        )
        # Look at AdminCreateUserConfig
        admin_create_user_config = response['UserPool']['AdminCreateUserConfig']
        # AllowAdminCreateUserOnly should be True
        if admin_create_user_config['AllowAdminCreateUserOnly'] == True:
            status = 'PASS'
        else:
            status = 'FAIL'
        return {
            "check_id": "COGNITO_003",
            "title": "Self Registration Enabled",
            "status": status,
            "severity": "HIGH",
            "description": "Self registration is enabled for this user pool, which can lead to unauthorized access if not properly monitored.",
            "remediation": "Set AllowAdminCreateUserOnly to True to disable self registration",
            "affected_resources": [user_pool_id]
        }
    
    except ClientError as e:
        error_message = e.response['Error']['Message']
        return {
            "check_id": "COGNITO_003",
            "title": "Self Registration Enabled",
            "status": 'ERROR',
            "severity": "HIGH",
            "description": f"Error checking self registration: {error_message}",
            "remediation": "Investigate the error and ensure the user pool ID is correct.",
            "affected_resources": [user_pool_id]
        }