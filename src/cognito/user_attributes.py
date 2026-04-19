import boto3
from botocore.exceptions import ClientError

# This function checks if sensitive attributes are writable for a given Cognito User Pool Client and returns a dictionary with the check results
def check_writable_attributes(cognito_client, user_pool_id, client_id):
    try:
        response = cognito_client.describe_user_pool_client(
            UserPoolId=user_pool_id,
            ClientId=client_id
        )
        writable_attributes = response['UserPoolClient'].get('WritableAttributes', [])

        sensitive_attributes = ['email', 'phone_number', 'custom:role', 'custom:isAdmin']

        vuln = []
        for attr in sensitive_attributes:
            if attr in writable_attributes:
                vuln.append(attr)

        if vuln:
            status = 'FAIL'
        else:            
            status = 'PASS'
        return {
            "check_id": "COGNITO_004",
            "title": "Sensitive Writable Attributes",
            "status": status,
            "severity": "HIGH",
            "vuln:": vuln,
            "description": "Sensitive attributes including email, phone_number, or custom role attributes are writable, allowing users to change their own attributes and potentially escalate privileges",
            "remediation": "Remove sensitive attributes from the list of writable attributes for this user pool client.",
            "affected_resources": [user_pool_id, client_id]
        }   
    
    except ClientError as e:
       error_message = e.response['Error']['Message']
       return {
            "check_id": "COGNITO_004",
            "title": "Sensitive Writable Attributes",
            "status": 'ERROR',
            "severity": "HIGH",
            "description": f"Error checking Sensitive Writable Attributes: {error_message}",
            "remediation": "Investigate the error and ensure the user pool ID and client ID are correct.",
            "affected_resources": [user_pool_id]
        }
