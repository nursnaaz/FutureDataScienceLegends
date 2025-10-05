import boto3
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Get environment variables without fallback values
AWS_REGION = os.getenv('AWS_REGION')
GATEWAY_IDENTIFIER = os.getenv('GATEWAY_IDENTIFIER')
LAMBDA_ARN = os.getenv('LAMBDA_ARN')
TARGET_NAME = os.getenv('TARGET_NAME')
TARGET_DESCRIPTION = os.getenv('TARGET_DESCRIPTION')

# Role ARN for assumption (add this to your .env file)
EXECUTION_ROLE_ARN = os.getenv('EXECUTION_ROLE_ARN')  # e.g., arn:aws:iam::455820316982:role/BedrockAgentcoreExecutionRole

def assume_role_and_get_client():
    """
    Assume IAM role and return a Bedrock Agentcore client with temporary credentials
    """
    if not EXECUTION_ROLE_ARN:
        print("EXECUTION_ROLE_ARN not found in environment variables. Using default credentials.")
        return boto3.client('bedrock-agentcore-control', region_name=AWS_REGION)
    
    try:
        # Create STS client
        sts_client = boto3.client('sts', region_name=AWS_REGION)
        
        # Assume the role
        response = sts_client.assume_role(
            RoleArn=EXECUTION_ROLE_ARN,
            RoleSessionName='BedrockAgentcoreSession'
        )
        
        # Extract temporary credentials
        credentials = response['Credentials']
        
        # Create Bedrock client with temporary credentials
        bedrock_client = boto3.client(
            'bedrock-agentcore-control',
            region_name=AWS_REGION,
            aws_access_key_id=credentials['AccessKeyId'],
            aws_secret_access_key=credentials['SecretAccessKey'],
            aws_session_token=credentials['SessionToken']
        )
        
        print(f"Successfully assumed role: {EXECUTION_ROLE_ARN}")
        return bedrock_client
        
    except Exception as e:
        print(f"Failed to assume role: {e}")
        print("Falling back to default credentials...")
        return boto3.client('bedrock-agentcore-control', region_name=AWS_REGION)

# Get the client (with role assumption if configured)
bedrock_agent_core_client = assume_role_and_get_client()

lambda_target_config = {
    "mcp": {
        "lambda": {
            "lambdaArn": LAMBDA_ARN,
            "toolSchema": {
                "inlinePayload": [
                    {
                        "name": "list_devices",
                        "description": "To list the devices. use action_name default parameter value as 'list_devices'",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "action_name": {
                                    "type": "string"
                                }
                            },
                            "required": ["action_name"]
                            }
                        },
                        {
                        "name": "get_device_settings",
                        "description": "To list the devices. use action_name default parameter value as 'get_device_settings'. You need to get teh device_id from the user",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "action_name": {
                                    "type": "string"
                                },
                                "device_id": {
                                    "type": "string"
                                }
                            },
                            "required": ["action_name","device_id"]
                            }
                        },
                        {
                        "name": "list_wifi_networks",
                        "description": "To list the devices. use action_name default parameter value as 'list_wifi_networks'. You need to get teh device_id from the user",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "action_name": {
                                    "type": "string"
                                },
                                "device_id": {
                                    "type": "string"
                                }
                            },
                            "required": ["action_name","device_id"]
                            }
                        },
                        {
                        "name": "list_users",
                        "description": "To list the devices. use action_name default parameter value as 'list_users'",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "action_name": {
                                    "type": "string"
                                }
                            },
                            "required": ["action_name"]
                            }
                        },
                        {
                        "name": "query_user_activity",
                        "description": "To list the devices. use action_name default parameter value as 'query_user_activity'. Please get start_date, end_date, user_id and activity_type from the user",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "action_name": {
                                    "type": "string"
                                },
                                "start_date": {
                                    "type": "string"
                                },
                                "end_date": {
                                    "type": "string"
                                },
                                "user_id": {
                                    "type": "string"
                                },
                                "activity_type": {
                                    "type": "string"
                                }               
                            },
                            "required": ["action_name","start_date","end_date"]
                            }
                        },
                        {
                        "name": "update_wifi_ssid",
                        "description": "To list the devices. use action_name default parameter value as 'update_wifi_ssid'. Get device_id, network_id and ssid from the user if not given in the context. ",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "action_name": {
                                    "type": "string"
                                },
                                "device_id": {
                                    "type": "string"
                                },
                                "network_id": {
                                    "type": "string"
                                },
                                "ssid": {
                                    "type": "string"
                                }
                            },
                            "required": ["action_name","device_id","network_id","ssid"]
                            }
                        },
                        {
                        "name": "update_wifi_security",
                        "description": "To list the devices. use action_name default parameter value as 'update_wifi_security'. Get device_id, network_id and security_type from the user if not given in the context.  ",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "action_name": {
                                    "type": "string"
                                },
                                 "device_id": {
                                    "type": "string"
                                },
                                 "network_id": {
                                    "type": "string"
                                },
                                 "security_type": {
                                    "type": "string"
                                }
                            },
                            "required": ["action_name","device_id","network_id","security_type"]
                            }
                        }
                ]
            }
        }
    }
}

credential_config = [ 
    {
        "credentialProviderType" : "GATEWAY_IAM_ROLE"
    }
]

try:
    print("Creating gateway target...")
    response = bedrock_agent_core_client.create_gateway_target(
        gatewayIdentifier=GATEWAY_IDENTIFIER,
        name=TARGET_NAME,
        description=TARGET_DESCRIPTION,
        credentialProviderConfigurations=credential_config, 
        targetConfiguration=lambda_target_config)
    
    print(f"✅ Gateway target created successfully!")
    print(f"Target ID: {response['targetId']}")
    
except Exception as e:
    print(f"❌ Error creating gateway target: {e}")
    print("\nPossible solutions:")
    print("1. Check IAM permissions (see IAM_PERMISSIONS_FIX.md)")
    print("2. Verify environment variables in .env file")
    print("3. Ensure the gateway exists and GATEWAY_IDENTIFIER is correct")