#!/bin/bash

# Deployment workflow script for Device Management System
# This script deploys all components in the correct order

set -e  # Exit on error

# Activate virtual environment if it exists
if [ -d "agentcore_env" ]; then
  echo "Activating virtual environment..."
  source agentcore_env/bin/activate
fi

# Function to display section headers
section() {
  echo ""
  echo "=========================================="
  echo "  $1"
  echo "=========================================="
  echo ""
}

# Function to check if a command exists
command_exists() {
  command -v "$1" >/dev/null 2>&1
}

# Check prerequisites
section "Checking prerequisites"

# Check for AWS CLI
if ! command_exists aws; then
  echo "Error: AWS CLI is not installed. Please install it first."
  exit 1
fi

# Check for Python
if command_exists python3; then
  PYTHON_CMD="python3"
  PIP_CMD="pip3"
elif command_exists python; then
  PYTHON_CMD="python"
  PIP_CMD="pip"
else
  echo "Error: Python is not installed. Please install Python 3.8 or higher."
  exit 1
fi

# Check for pip
if ! command_exists $PIP_CMD && ! command_exists pip; then
  echo "Error: pip is not installed. Please install it first."
  exit 1
fi

# Use pip3 if available, otherwise use pip
if command_exists pip3; then
  PIP_CMD="pip3"
elif command_exists pip; then
  PIP_CMD="pip"
fi

# Check AWS credentials
if ! aws sts get-caller-identity >/dev/null 2>&1; then
  echo "Error: AWS credentials not configured or invalid. Please run 'aws configure'."
  exit 1
fi

echo "All prerequisites satisfied."

# Step 1: Deploy Device Management Lambda
section "Step 1: Deploying Device Management Lambda"

cd device-management
echo "Installing Python dependencies..."
$PIP_CMD install -r requirements.txt

echo "Deploying Lambda function..."
chmod +x deploy.sh
./deploy.sh

# Get the Lambda ARN from the output file or AWS CLI
if [ -f lambda_arn.txt ]; then
  LAMBDA_ARN=$(grep LAMBDA_ARN lambda_arn.txt | cut -d= -f2)
  echo "Lambda ARN: $LAMBDA_ARN"
else
  # Fallback: get Lambda ARN directly from AWS
  LAMBDA_FUNCTION_NAME=${LAMBDA_FUNCTION_NAME:-"DeviceManagementLambda"}
  LAMBDA_ARN=$(aws lambda get-function --function-name "$LAMBDA_FUNCTION_NAME" --region us-west-2 --query 'Configuration.FunctionArn' --output text 2>/dev/null)
  if [ -z "$LAMBDA_ARN" ]; then
    echo "Error: Lambda ARN not found. Please ensure the Lambda function was deployed successfully."
    exit 1
  fi
  echo "Lambda ARN (from AWS): $LAMBDA_ARN"
fi

cd ..

# Step 2: Create Gateway
section "Step 2: Creating Gateway"

cd gateway

# Check if .env file exists, if not create it
if [ ! -f .env ]; then
  echo "Creating .env file for gateway..."
  
  # Create basic .env file structure
  cat > .env << EOF
# AWS and endpoint configuration
AWS_REGION=us-west-2
ENDPOINT_URL=https://bedrock-agentcore-control.us-west-2.amazonaws.com

# Lambda configuration (from device-management module)
LAMBDA_ARN=$LAMBDA_ARN

# Target configuration
GATEWAY_IDENTIFIER=your-gateway-identifier
TARGET_NAME=device-management-target
TARGET_DESCRIPTION=List, Update device management activities

# Gateway creation configuration
GATEWAY_NAME=Device-Management-Gateway
GATEWAY_DESCRIPTION=Device Management Gateway
EOF
  
  echo "Please edit the gateway/.env file to set your Cognito details and other required values."
  echo "Then run this script again."
  exit 0
else
  # Update existing .env file with Lambda ARN
  echo "Updating existing .env file with Lambda ARN..."
  if grep -q "^LAMBDA_ARN=" .env; then
    # Update existing LAMBDA_ARN line
    if [[ "$OSTYPE" == "darwin"* ]]; then
      sed -i '' "s|^LAMBDA_ARN=.*|LAMBDA_ARN=$LAMBDA_ARN|g" .env
    else
      sed -i "s|^LAMBDA_ARN=.*|LAMBDA_ARN=$LAMBDA_ARN|g" .env
    fi
  else
    # Add LAMBDA_ARN to the file
    echo "" >> .env
    echo "# Lambda configuration (from device-management module)" >> .env
    echo "LAMBDA_ARN=$LAMBDA_ARN" >> .env
  fi
fi

echo "Installing Python dependencies for gateway..."
$PIP_CMD install -r requirements.txt

echo "Checking for existing gateway..."
GATEWAY_NAME=$(grep GATEWAY_NAME .env | cut -d= -f2)
EXISTING_GATEWAY=$(aws bedrock-agentcore-control list-gateways --query "items[?name=='$GATEWAY_NAME']" --output text --region us-west-2 2>/dev/null)

if [ -n "$EXISTING_GATEWAY" ]; then
  # Get existing gateway details
  GATEWAY_ID=$(aws bedrock-agentcore-control list-gateways --query "items[?name=='$GATEWAY_NAME'].gatewayId" --output text --region us-west-2)
  
  echo "Gateway '$GATEWAY_NAME' already exists!"
  echo "Using existing Gateway ID: $GATEWAY_ID"
  
  # Update .env file with existing gateway info
  if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s|GATEWAY_IDENTIFIER=.*|GATEWAY_IDENTIFIER=$GATEWAY_ID|g" .env
    sed -i '' "s|GATEWAY_ID=.*|GATEWAY_ID=$GATEWAY_ID|g" .env
  else
    sed -i "s|GATEWAY_IDENTIFIER=.*|GATEWAY_IDENTIFIER=$GATEWAY_ID|g" .env
    sed -i "s|GATEWAY_ID=.*|GATEWAY_ID=$GATEWAY_ID|g" .env
  fi
else
  echo "Creating gateway..."
  $PYTHON_CMD create_gateway.py
  
  # Get the Gateway ID from the created gateway
  GATEWAY_ID=$(aws bedrock-agentcore-control list-gateways --query "items[?name=='$GATEWAY_NAME'].gatewayId" --output text --region us-west-2)
  
  if [ -z "$GATEWAY_ID" ]; then
    echo "Error: Failed to get Gateway ID."
    exit 1
  fi
  
  echo "Gateway ID: $GATEWAY_ID"
  
  # Update the .env file with the Gateway ID
  if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s|GATEWAY_IDENTIFIER=.*|GATEWAY_IDENTIFIER=$GATEWAY_ID|g" .env
  else
    sed -i "s|GATEWAY_IDENTIFIER=.*|GATEWAY_IDENTIFIER=$GATEWAY_ID|g" .env
  fi
fi

echo "Creating gateway target using AWS CLI..."

# Create target configuration JSON file
cat > target-config.json << 'EOF'
{
  "mcp": {
    "lambda": {
      "lambdaArn": "LAMBDA_ARN_PLACEHOLDER",
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
              "required": ["action_name", "device_id"]
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
              "required": ["action_name", "device_id"]
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
              "required": ["action_name", "start_date", "end_date"]
            }
          },
          {
            "name": "update_wifi_ssid",
            "description": "To list the devices. use action_name default parameter value as 'update_wifi_ssid'. Get device_id, network_id and ssid from the user if not given in the context.",
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
              "required": ["action_name", "device_id", "network_id", "ssid"]
            }
          },
          {
            "name": "update_wifi_security",
            "description": "To list the devices. use action_name default parameter value as 'update_wifi_security'. Get device_id, network_id and security_type from the user if not given in the context.",
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
              "required": ["action_name", "device_id", "network_id", "security_type"]
            }
          }
        ]
      }
    }
  }
}
EOF

# Replace the Lambda ARN placeholder with the actual ARN
if [[ "$OSTYPE" == "darwin"* ]]; then
  sed -i '' "s|LAMBDA_ARN_PLACEHOLDER|$LAMBDA_ARN|g" target-config.json
else
  sed -i "s|LAMBDA_ARN_PLACEHOLDER|$LAMBDA_ARN|g" target-config.json
fi

# Create credential configuration JSON file
cat > credential-config.json << 'EOF'
[
  {
    "credentialProviderType": "GATEWAY_IAM_ROLE"
  }
]
EOF

# Check if target already exists
EXISTING_TARGET=$(aws bedrock-agentcore-control list-gateway-targets --gateway-identifier "$GATEWAY_ID" --region us-west-2 --query "items[?name=='device-management-target'].targetId" --output text 2>/dev/null || echo "")

if [ -n "$EXISTING_TARGET" ]; then
  echo "Gateway target 'device-management-target' already exists with ID: $EXISTING_TARGET"
else
  # Create gateway target using AWS CLI
  TARGET_RESPONSE=$(aws bedrock-agentcore-control create-gateway-target \
    --gateway-identifier "$GATEWAY_ID" \
    --name "device-management-target" \
    --description "List, Update device management activities" \
    --credential-provider-configurations file://credential-config.json \
    --target-configuration file://target-config.json \
    --region us-west-2 2>&1)
  
  if [ $? -eq 0 ]; then
    TARGET_ID=$(echo "$TARGET_RESPONSE" | grep -o '"targetId": "[^"]*"' | cut -d'"' -f4)
    echo "✅ Gateway target created successfully!"
    echo "Target ID: $TARGET_ID"
  else
    echo "❌ Failed to create gateway target:"
    echo "$TARGET_RESPONSE"
    echo ""
    echo "This might be due to IAM permission propagation delay."
    echo "Please see gateway/IAM_PERMISSIONS_FIX.md for troubleshooting steps."
    exit 1
  fi
fi

# Clean up temporary files
rm -f target-config.json credential-config.json

# Update .env with Gateway ARN and ID for observability
GATEWAY_ARN=$(aws bedrock-agentcore-control list-gateways --query "items[?gatewayId=='$GATEWAY_ID'].gatewayArn" --output text --region us-west-2)
if ! grep -q "^GATEWAY_ARN=" .env; then
  echo "GATEWAY_ARN=$GATEWAY_ARN" >> .env
else
  if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s|GATEWAY_ARN=.*|GATEWAY_ARN=$GATEWAY_ARN|g" .env
  else
    sed -i "s|GATEWAY_ARN=.*|GATEWAY_ARN=$GATEWAY_ARN|g" .env
  fi
fi
if ! grep -q "^GATEWAY_ID=" .env; then
  echo "GATEWAY_ID=$GATEWAY_ID" >> .env
fi

echo "Setting up gateway observability..."
if $PYTHON_CMD gateway_observability.py; then
  echo "✅ Gateway observability configured successfully"
else
  echo "⚠️  Gateway observability setup skipped (optional)"
  echo "You can run 'cd gateway && python3 gateway_observability.py' manually later if needed"
fi

cd ..

# Step 3: Deploy Agent Runtime
section "Step 3: Deploying Agent Runtime"

cd agent-runtime

# Check if .env file exists, if not create it
if [ ! -f .env ]; then
  echo "Creating .env file for agent runtime..."
  cp .env.example .env
  
  # Update the Gateway URL in the .env file
  GATEWAY_URL="https://$GATEWAY_ID.gateway.bedrock-agentcore.us-west-2.amazonaws.com"
  if [[ "$OSTYPE" == "darwin"* ]]; then
    sed -i '' "s|MCP_SERVER_URL=.*|MCP_SERVER_URL=$GATEWAY_URL|g" .env
  else
    sed -i "s|MCP_SERVER_URL=.*|MCP_SERVER_URL=$GATEWAY_URL|g" .env
  fi
  
  echo "Please edit the agent-runtime/.env file to set your Cognito details and other required values."
  echo "Then run this script again."
  exit 0
fi

# Update requirements-runtime.txt with observability packages
echo "Updating requirements-runtime.txt with observability packages..."
if ! grep -q "aws_opentelemetry_distro_genai_beta" requirements-runtime.txt; then
  echo "aws_opentelemetry_distro_genai_beta>=0.1.2" >> requirements-runtime.txt
fi
if ! grep -q "aws-xray-sdk" requirements-runtime.txt; then
  echo "aws-xray-sdk>=2.12.0" >> requirements-runtime.txt
fi
if ! grep -q "watchtower" requirements-runtime.txt; then
  echo "watchtower>=3.0.1" >> requirements-runtime.txt
fi
if ! grep -q "opentelemetry-instrumentation-requests" requirements-runtime.txt; then
  echo "opentelemetry-instrumentation-requests>=0.40b0" >> requirements-runtime.txt
fi
# Note: opentelemetry-instrumentation-boto3 package doesn't exist, skip it
# if ! grep -q "opentelemetry-instrumentation-boto3" requirements-runtime.txt; then
#   echo "opentelemetry-instrumentation-boto3>=0.40b0" >> requirements-runtime.txt
# fi

# Update Dockerfile with OpenTelemetry configuration
echo "Updating Dockerfile with OpenTelemetry configuration..."
cat > Dockerfile << 'EOF'
FROM public.ecr.aws/docker/library/python:3.12-slim
WORKDIR /app

# Copy entire project (respecting .dockerignore)
COPY . .

# Install dependencies
RUN python -m pip install --no-cache-dir -r requirements-runtime.txt

# Install AWS OpenTelemetry Distro for GenAI
RUN python -m pip install aws_opentelemetry_distro_genai_beta>=0.1.2

# Install AWS X-Ray SDK
RUN python -m pip install aws-xray-sdk

# Set AWS region environment variable
ENV AWS_REGION=us-west-2
ENV AWS_DEFAULT_REGION=us-west-2

# Set OpenTelemetry environment variables
ENV OTEL_PYTHON_DISABLED_INSTRUMENTATIONS=""
ENV OTEL_METRICS_EXPORTER="otlp"
ENV OTEL_TRACES_EXPORTER="otlp"
ENV OTEL_EXPORTER_OTLP_PROTOCOL="http/protobuf"
ENV OTEL_RESOURCE_ATTRIBUTES="service.name=device-management-agent"

# Signal that this is running in Docker for host binding logic
ENV DOCKER_CONTAINER=1

# Create non-root user
RUN useradd -m -u 1000 bedrock_agentcore
USER bedrock_agentcore

EXPOSE 8080

# Use OpenTelemetry instrumentation to run the application
CMD ["opentelemetry-instrument", "python3.12", "-m", "strands-agent-runtime"]
EOF

# Update .bedrock_agentcore.yaml to ensure observability is enabled
echo "Ensuring observability is enabled in .bedrock_agentcore.yaml..."
if [ -f .bedrock_agentcore.yaml ]; then
  # Check if observability section exists and update it
  if grep -q "observability:" .bedrock_agentcore.yaml; then
    # Use awk to update the observability section
    awk '
    /observability:/ {
      print "      observability:";
      print "        enabled: true";
      print "        cloudwatch:";
      print "          log_group: \"/aws/bedrock-agentcore/device-management-agent\"";
      print "        xray:";
      print "          trace_enabled: true";
      found=1;
      next;
    }
    /enabled:/ && found==1 { found=0; next; }
    found==1 { next; }
    { print }
    ' .bedrock_agentcore.yaml > .bedrock_agentcore.yaml.tmp && mv .bedrock_agentcore.yaml.tmp .bedrock_agentcore.yaml
  fi
fi

echo "Installing Python dependencies for agent runtime..."
$PIP_CMD install -r requirements-runtime.txt

echo "Deploying agent runtime..."
$PYTHON_CMD strands_agent_runtime_deploy.py

cd ..

# Step 4: Update frontend configuration
section "Step 4: Updating frontend configuration"

# Get the Gateway URL
GATEWAY_URL="https://$GATEWAY_ID.gateway.bedrock-agentcore.us-west-2.amazonaws.com"
echo "Gateway URL: $GATEWAY_URL"

# Create .env file for frontend if it doesn't exist
if [ ! -f frontend/.env ]; then
  echo "Creating .env file for frontend..."
  echo "MCP_SERVER_URL=$GATEWAY_URL" > frontend/.env
  echo "COGNITO_DOMAIN=$(grep FRONTEND_COGNITO_DOMAIN .env | cut -d= -f2)" >> frontend/.env
  echo "COGNITO_CLIENT_ID=$(grep FRONTEND_COGNITO_APP_CLIENT_ID .env | cut -d= -f2)" >> frontend/.env
  
  echo "Please complete the frontend/.env file with any missing values."
fi

# Step 5: Move chat_app_bedrock to frontend directory
section "Step 5: Moving chat_app_bedrock to frontend directory"

if [ -d chat_app_bedrock ] && [ ! -d frontend/chat_app_bedrock ]; then
  echo "Moving chat_app_bedrock to frontend directory..."
  mv chat_app_bedrock frontend/
fi

section "Deployment completed successfully!"
echo "Next steps:"
echo "1. Generate synthetic data: cd device-management && python synthetic_data.py"
echo "2. Set up the frontend: Follow instructions in frontend/README.md"
echo "3. Test the system: Use the Q CLI or the chat application to interact with the MCP server"
echo "4. Monitor the system: Check CloudWatch Logs and X-Ray traces for observability data"
echo ""
echo "Gateway URL: $GATEWAY_URL"
echo ""
echo "Observability Information:"
echo "- CloudWatch Log Group: /aws/bedrock-agentcore/device-management-agent"
echo "- X-Ray Traces: Enabled for the agent runtime"
echo "- Metrics: Available in CloudWatch Metrics under the 'device-management-agent' namespace"
echo ""
echo "To view logs: https://console.aws.amazon.com/cloudwatch/home?region=us-west-2#logsV2:log-groups"
echo "To view traces: https://console.aws.amazon.com/xray/home?region=us-west-2#/traces"
