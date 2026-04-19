import argparse
from utils.aws_session import start_aws_session
from src.cognito.mfa_check import check_mfa
from src.cognito.unauth_check import check_unauthenticated_access
from src.cognito.self_registration import check_self_registration
from src.cognito.user_attributes import check_writable_attributes

def parse_args():
    parser = argparse.ArgumentParser(description='Cognito Security Scanner')
    parser.add_argument('--profile', required=True, help='AWS profile name')
    parser.add_argument('--region', required=True, help='AWS region')
    parser.add_argument('--user-pool-id', required=True)
    parser.add_argument('--identity-pool-id', required=True)
    parser.add_argument('--client-id', required=True)
    return parser.parse_args()

def main():
    args = parse_args()
    
    # Start session and create clients
    session = start_aws_session(args.profile, args.region)
    cognito_client = session.client('cognito-idp')
    identity_client = session.client('cognito-identity')
    
    # Run all checks
    results = [
        check_mfa(cognito_client, args.user_pool_id),
        check_unauthenticated_access(identity_client, args.identity_pool_id),
        check_self_registration(cognito_client, args.user_pool_id),
        check_writable_attributes(cognito_client, args.user_pool_id, args.client_id)
    ]
    
    for result in results:
        print(result)

if __name__ == '__main__':
    main()