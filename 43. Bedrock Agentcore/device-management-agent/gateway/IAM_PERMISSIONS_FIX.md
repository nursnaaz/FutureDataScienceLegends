# IAM Permissions Fix for Bedrock Agentcore

## Problem
You're encountering the following error when running `device-management-target.py`:

```
botocore.errorfactory.AccessDeniedException: An error occurred (AccessDeniedException) when calling the CreateGatewayTarget operation: User: arn:aws:iam::455820316982:user/noordeen is not authorized to perform: bedrock-agentcore:CreateGatewayTarget
```

## Solution Options

### Option 1: Attach Policy to IAM User (Recommended)

1. **Create the IAM Policy** (already done - see `iam-policy.json`)

2. **Attach Policy via AWS CLI:**
   ```bash
   # First, create the policy in your AWS account
   aws iam create-policy \
     --policy-name BedrockAgentcoreFullAccess \
     --policy-document file://gateway/iam-policy.json \
     --description "Full access to Bedrock Agentcore services"
   
   # Then attach it to your user
   aws iam attach-user-policy \
     --user-name noordeen \
     --policy-arn arn:aws:iam::455820316982:policy/BedrockAgentcoreFullAccess
   ```

3. **Attach Policy via AWS Console:**
   - Go to AWS IAM Console → Users → noordeen
   - Click "Add permissions" → "Attach policies directly"
   - Click "Create policy" → JSON tab
   - Copy and paste the contents of `gateway/iam-policy.json`
   - Name the policy: `BedrockAgentcoreFullAccess`
   - Save and attach to user

### Option 2: Use IAM Role with AssumeRole

If you prefer using roles instead of directly attaching permissions to your user:

1. **Create an IAM Role** (via AWS Console or CLI):
   ```bash
   # Create trust policy for the role
   cat > trust-policy.json << EOF
   {
     "Version": "2012-10-17",
     "Statement": [
       {
         "Effect": "Allow",
         "Principal": {
           "AWS": "arn:aws:iam::455820316982:user/noordeen"
         },
         "Action": "sts:AssumeRole"
       }
     ]
   }
   EOF
   
   # Create the role
   aws iam create-role \
     --role-name BedrockAgentcoreExecutionRole \
     --assume-role-policy-document file://trust-policy.json
   
   # Attach the policy to the role
   aws iam create-policy \
     --policy-name BedrockAgentcoreFullAccess \
     --policy-document file://gateway/iam-policy.json
   
   aws iam attach-role-policy \
     --role-name BedrockAgentcoreExecutionRole \
     --policy-arn arn:aws:iam::455820316982:policy/BedrockAgentcoreFullAccess
   ```

2. **Modify the script to use the role** - see `device-management-target-with-role.py`

### Option 3: Administrator Access (Not Recommended for Production)

If you need quick testing access, you can temporarily attach AdministratorAccess:

```bash
aws iam attach-user-policy \
  --user-name noordeen \
  --policy-arn arn:aws:iam::aws:policy/AdministratorAccess
```

**⚠️ Warning:** This gives full AWS access. Remove it after testing!

## Verification

After applying any of the above solutions, verify the permissions:

```bash
# Check attached policies
aws iam list-attached-user-policies --user-name noordeen

# Test the specific permission
aws bedrock-agentcore-control list-gateways --region us-west-2
```

## Next Steps

1. Apply one of the solutions above
2. Run the script again: `python gateway/device-management-target.py`
3. The script should now successfully create the gateway target

## Required Permissions Explained

The IAM policy includes these key permissions:
- `bedrock-agentcore:*` - Full access to Bedrock Agentcore operations
- `iam:PassRole` - Required to pass roles to Bedrock services
- `lambda:InvokeFunction` - Required for Lambda integration
- `logs:*` - Required for CloudWatch logging