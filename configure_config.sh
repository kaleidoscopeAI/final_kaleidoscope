#!/bin/bash

# Set the values for your configuration
AWS_ACCESS_KEY_ID="AKIA4WJPWX75TYA35SVU"  # Replace with your actual Access Key ID
AWS_SECRET_ACCESS_KEY="M496HYeQ4JzOdRtsdlPn6Bbl2A54rEEgfRo0WV/N"  # Replace with your actual Secret Access Key
GODADDY_API_KEY="EnvironmentNameKeyCreatedActionsOTEartificialthinker.com3mM44Ywf1677ab_Hx1wV7Hy6JjiXcPeGiRQzL14"  # Replace with your actual GoDaddy API Key
GODADDY_API_SECRET="Productionartificialthinker.comh1ULrdTohqt8_EKjfAyyafQFKFVbZ5CdKzb"  # Replace with your actual GoDaddy API Secret
REGION="us-east-2"  # Replace with your actual AWS region
VPC_ID="your_vpc_id"  # Replace with your actual VPC ID
SUBNET_IDS=("subnet-1234567890abcdef0" "subnet-0fedcba9876543210")  # Replace with your actual subnet IDs
SECURITY_GROUP_IDS=("sg-1234567890abcdef0" "sg-0fedcba9876543210")  # Replace with your actual security group IDs
REDIS_URL="redis://your-redis-endpoint:6379"  # Replace with your actual Redis endpoint
HEALTH_CHECK_PATH="/health"  # Replace with your actual health check path

# Create the config.ini file
cat > config.ini <<EOF
[aws]
region = $REGION
ecr_repository_name = kaleidoscope-backend
stack_name = kaleidoscope-stack
vpc = $VPC_ID
subnets = ${SUBNET_IDS[@]}
security_groups = ${SECURITY_GROUP_IDS[@]}

[godaddy]
api_key = $GODADDY_API_KEY
api_secret = $GODADDY_API_SECRET
domain = artificialthinker.com

[redis]
url = $REDIS_URL

[healthcheck]
path = $HEALTH_CHECK_PATH
EOF

echo "config.ini created successfully!"
