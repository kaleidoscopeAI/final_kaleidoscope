#!/bin/bash

# Set variables (customize these)
REGION="us-east-1"
ECR_REPOSITORY_NAME="kaleidoscope-backend"
STACK_NAME="kaleidoscope-stack" 

# Build and push Docker images
docker-compose build
docker tag kaleidoscope-backend:latest ${AWS::Account}.dkr.ecr.${AWS::Region}.amazonaws.com/${ECR_REPOSITORY_NAME}:latest
docker push ${AWS::Account}.dkr.ecr.${AWS::Region}.amazonaws.com/${ECR_REPOSITORY_NAME}:latest

# Deploy CloudFormation stack
aws cloudformation deploy \
  --template-file template.yml \
  --stack-name $STACK_NAME \
  --region $REGION \
  --capabilities CAPABILITY_IAM # Required for IAM resources

# Get Load Balancer DNS name
LOAD_BALANCER_DNS=$(aws cloudformation describe-stacks \
  --stack-name $STACK_NAME \
  --region $REGION \
  --query 'Stacks.Outputs[?OutputKey==`LoadBalancerDNS`].OutputValue' \
  --output text)

# Update GoDaddy DNS
python goDaddy_dns_setup.py $LOAD_BALANCER_DNS
