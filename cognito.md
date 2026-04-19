## AWS Cognito

AWS Cognito is a fully managed service that helps developers manage user authentication and identity in applications. It allows you to add sign-up, sign-in, and access control to your applications quickly and securely, without having to build these features from scratch. Cognito User Pools & Cognito Identity Pools are the core features in AWS Cognito. User Pools allow you to authenticate and authorize user for an app or API. Identity pools and can be used to allow users to access AWS resources. 

An area of interest for an attacker from a *user pool* perspective would be to inspect the source code in a web application via the browser using inspect element. You can look for the initilization of the Cognito service and would be able to get the string that contains the user pool client id. This may lead to an attacker signing up for an AWS account using the cli and leveraging the Cognito User Pool ID

This is similar from an *Identity Pool* perspective. If a user is able to successfully gain access to an AWS Account, an attacker can potentially perform actions in that account. Identity pools map to IAM roles, so if the role is overly permissive an attack but be able to use that to perform actions such as gain access to sensitive data and role chain their way to different AWS accounts via role traversal. 

Cognito allows for managed *MFA*. The standard out of the box mfa solution in Cognito is SMS based. An attacker can potentially leverage sim swapping as an attack vector. An attacker can gain access to a phone number via a mobile carrier via social engineering, trigger the auth flow, and get an sms code to be able to access the system. 

*User Attributes* are pieces of information that help identify users such as name and email addresses. These are put directly into the ID tokens via JWT. An attacker can potentially leverage this to reassign access and perform priviledge escalation. If a developer has marked a sensitive attribute as mutable in the User Pool schema, they can call the AWS api UpdateUserAttributes to change their own attribute values. 

AWS Cognito can link to an *External Federation* provider such as Okta, Active Directory etc. Group assignments in Cognito are IAM roles based. If group assignments for users are overly permissive, and they are synced to Cognito via the IdP and mapped to a Cognito group, this can lead to a potential attacker gaining unauthorized access to the AWS environment or the applications running using Cognito.

## 5 Common Misconfigurations for AWS Cognito

1. Unauthenticated Identity Pool Access. Idenity Pools are revealed in JS source code via the web browser. An attacker can potentially call GetID to get the IdentityID, then GetCredentialsForIdentity and retrieve temporary AWS credentials with AWS Access Key, Secret Key, and Session Token. This can lead unauthenticated access to AWS with no login. AWS reccomends to disable unauthenticated access in Identity Pool settings unless explicitly required. Also, apply least priviledge to IAM roles.

2. Cognito User Pools allow for self registration. If "Allow self-registration" remains enabled, anyone can create an account via the SignUp API, even if the frontend lacks a "Sign up" button. If an attacker gets the identity pool id via the browser, they can call the api call aws cognito-idp sign-up and sign up without a sign up button. They can then login and get JWT token. If the identity pools are linked, they can exchange JWT credentials for temporary AWS credentials. If the Cognito group that they land in is overly permissive, they can try to enumarate their IAM permissions.  AWS reccomends to disable Self Service Registration or use a pre sign up Lambda trigger. 

3. MFA by default is turned off in Cognito. It needs to be turned on. When turned on the default is SMS based. An attacker can potentially leverage sim swapping as an attack vector. An attacker can gain access to a phone number via a mobile carrier via social engineering, trigger the auth flow, and get an sms code to be able to access the system. AWS reccomends to use TOTP Authenticator Apps such as Google Authenticator instead of SMS. These are not vulernarable to SMS based attacks. 


4. If an app allows users to modify attributes, an attacker can change their email to match a victims email and gain access without needing a password. AWS reccomends to always use the sub claim as a unique identifier (UUID) which cannot be modified and mark sensitive attributes as immutable.

5. Not validating JWT tokens effectively. When a user authenticates via AWS Cognito, they are issued an ID token with claims about the authenticated user such as name, email, phone number. AWS reccomends these tokens be validated via aws-jwt-verify library. 




