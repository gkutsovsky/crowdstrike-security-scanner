## Project Structure

```
.
├── src/
│   └── cognito/
│       ├── __init__.py
│       ├── mfa_check.py            # Check: MFA not enforced
│       ├── self_registration.py    # Check: Open self-registration
│       ├── unauth_check.py         # Check: Unauthenticated identity pool access
│       └── user_attributes.py      # Check: Sensitive writable attributes
├── utils/
│   ├── __init__.py
│   └── aws_client.py               # Boto3 session utility
├── main.py                         # Main runner and output formatter
├── cognito.md                      # Security research findings (Part 2)
└── README.md
```

---

## Installation

**1. Clone the repository**
```bash
git clone <your-repo-url>
cd <repo-name>
```

**2. Create and activate a virtual environment**
```bash
python3 -m venv venv
source venv/bin/activate        
venv\Scripts\activate          
```

**3. Install dependencies**
```bash
pip install boto3
```

**4. Configure AWS credentials**
```bash
aws configure --profile <your-profile>
```

---

## Usage

Run the scanner from the project root:

```bash
python main.py \
  --profile <aws-profile> \
  --region <aws-region> \
  --user-pool-id <user-pool-id> \
  --identity-pool-id <identity-pool-id> \
  --client-id <app-client-id>
```

## Checks Implemented

| Check ID | Title | Severity | API Call |
|---|---|---|---|
| COGNITO_001 | Unauthenticated Identity Pool Access | CRITICAL | `describe_identity_pool` |
| COGNITO_002 | MFA Not Enforced | HIGH | `describe_user_pool` |
| COGNITO_003 | Self Registration Enabled | HIGH | `describe_user_pool` |
| COGNITO_004 | Sensitive Writable Attributes | HIGH | `describe_user_pool_client` |

---