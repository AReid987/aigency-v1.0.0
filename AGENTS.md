+++
# --- Basic Metadata ---
id = "AGENTS-LAMBDA-DOCUMENTATION"
title = "AWS Lambda Functions - Specialized AGENTS.md Documentation"
context_type = "documentation"
scope = "AI Agency project Lambda function patterns, configurations, and best practices"
target_audience = ["developers", "devops", "architects", "cloud-aws"]
granularity = "comprehensive"
status = "active" # << ACCURATE STATUS >>
last_updated = "2025-08-29" # << ACCURATE DATE >>
# version = "1.0.0"
tags = [
    "aws-lambda",
    "serverless",
    "event-driven",
    "cloudformation",
    "api-gateway",
    "iac",
    "security",
    "monitoring",
    "cost-optimization",
    "ci-cd"
]
# relevance = "Critical: Documents project-specific Lambda patterns and best practices"
# related_context = []
+++

# AWS Lambda Functions - Specialized AGENTS.md Documentation

## Overview

This documentation establishes comprehensive patterns and best practices for AWS Lambda functions within the AI Agency project. It covers serverless deployment patterns, security configurations, event-driven architectures, CloudFormation/Serverless Framework conventions, API Gateway integrations, and Lambda-specific error handling and logging strategies.

Based on analysis of the project's existing AWS knowledge base, this guide incorporates the [Well-Architected Framework pillars](../../.ruru/modes/cloud-aws/kb/02-architecture-design.md) and establishes project-specific conventions that deviate from standard AWS Lambda practices where necessary for our operational requirements.

---

## 1. Serverless Deployment Patterns and Configurations

### Core Lambda Configuration Standards

#### Function Configuration Template

**Standard Deployment Configuration:**
```yaml
# CloudFormation Lambda Function Resource
MyFunction:
  Type: AWS::Lambda::Function
  Properties:
    FunctionName: !Sub "${Environment}-my-function-${AWS::StackName}"
    Runtime: python3.12  # Project standard
    Handler: lambda_function.handler
    MemorySize: 256  # Start conservative, scale as needed
    Timeout: 300  # 5 minutes default
    ReservedConcurrentExecutions: 100  # Prevent unbounded concurrency
    Environment:
      Variables:
        LOG_LEVEL: INFO
        POWERTOOLS_SERVICE_NAME: !Ref AWS::StackName
        POWERTOOLS_LOGGER_LOG_EVENT: FALSE
    Layers:
      - !Ref LambdaPowerToolsLayer
    VpcConfig:
      SecurityGroupIds:
        - !GetAtt LambdaSecurityGroup.GroupId
      SubnetIds: !Ref PrivateSubnets
    TracingConfig:
      Mode: Active
    Tags:
      - Key: Environment
        Value: !Ref Environment
      - Key: Service
        Value: !Ref AWS::StackName
    DeadLetterConfig:
      TargetArn: !GetAtt FunctionDeadLetterQueue.Arn
```

#### Runtime Selection Principles

1. **Python 3.12** - Project standard for new functions
2. **Use of Lambda Powertools** - Mandatory for observability and utilities
3. **Custom Runtime** - For specialized performance requirements only
4. **Arm64 Architecture** - Default for cost optimization (use x86_64 only when required)

### Packaging and Deployment Strategies

#### Source Code Organization
```
lambda/
├── src/
│   ├── handlers/
│   ├── services/
│   ├── utils/
│   └── models/
├── tests/
│   ├── unit/
│   └── integration/
├── infrastructure/
│   ├── stack.yaml  # CloudFormation template
│   └── parameters.json
├── requirements.txt
├── makefile
└── Dockerfile  # For containerized deployments
```

#### Lambda Layers Strategy

**Standard Layers:**
1. **Lambda Powertools Layer** - Observability and utilities
2. **SDKs Layer** - Common third-party dependencies
3. **Shared Libraries Layer** - Project-specific utilities
4. **Database Connection Layer** - Database connection pooling

---

## 2. Lambda-Specific Environment Variables and Secrets Management

### Environment Variable Naming Convention

```python
# Standard environment variable patterns
import os

class EnvironmentVariables:
    @staticmethod
    def get_db_connection_string():
        """Database connection with secure pattern"""
        required_vars = [
            'DB_HOST',
            'DB_PORT',
            'DB_NAME',
            'DB_USER',
            'DB_PASSWORD'  # Retrieved securely via SSM
        ]

        # Validate all required variables exist
        for var in required_vars:
            if not os.getenv(var):
                raise EnvironmentError(f"Missing required environment variable: {var}")

        return f"postgresql://{os.getenv('DB_USER')}:{get_ssm_parameter('/db/password')}@{os.getenv('DB_HOST')}:{os.getenv('DB_PORT')}/{os.getenv('DB_NAME')}"

    @staticmethod
    def get_service_config():
        """Service-specific configuration"""
        return {
            'log_level': os.getenv('LOG_LEVEL', 'INFO'),
            'timeout': int(os.getenv('TIMEOUT_SECONDS', '30')),
            'retry_attempts': int(os.getenv('RETRY_ATTEMPTS', '3')),
            'batch_size': int(os.getenv('BATCH_SIZE', '10'))
        }
```

### Secrets Management Patterns

#### Parameter Store (SSM) Integration
```python
import boto3
from functools import lru_cache

class SecretsManager:
    def __init__(self):
        self.client = boto3.client('ssm', region_name=get_env_var('AWS_REGION'))
        self.secrets_client = boto3.client('secretsmanager')

    @lru_cache(maxsize=128)  # Cache to reduce API calls
    def get_parameter(self, name: str, with_decryption: bool = True) -> str:
        """Retrieve SSM parameter with error handling and caching"""
        try:
            response = self.client.get_parameter(
                Name=name,
                WithDecryption=with_decryption
            )
            return response['Parameter']['Value']
        except self.client.exceptions.ParameterNotFound:
            logger.warning(f"SSM Parameter not found: {name}")
            raise
        except Exception as e:
            logger.error(f"Failed to retrieve SSM parameter {name}: {str(e)}")
            raise

    def get_secret(self, secret_name: str) -> dict:
        """Retrieve secret from Secrets Manager"""
        try:
            response = self.secrets_client.get_secret_value(SecretId=secret_name)
            return json.loads(response['SecretString'])
        except Exception as e:
            logger.error(f"Failed to retrieve secret {secret_name}: {str(e)}")
            raise
```

#### CloudFormation Environment Variable Pattern
```yaml
Parameters:
  DBUsername:
    Type: String
  DBPassword:
    Type: AWS::SSM::Parameter::Value<String>
    Default: '/database/password'

  EnvironmentMap:
    Type: Map
    Default:
      Development:
        LOG_LEVEL: DEBUG
        TIMEOUT_SECONDS: 60
      Production:
        LOG_LEVEL: INFO
        TIMEOUT_SECONDS: 30

Resources:
  MyFunction:
    Type: AWS::Lambda::Function
    Properties:
      Environment:
        Variables:
          DB_USER: !Ref DBUsername
          DB_PASSWORD: !Ref DBPassword
          LOG_LEVEL: !FindInMap [EnvironmentMap, !Ref Environment, LOG_LEVEL]
          POWERTOOLS_SERVICE_NAME: !Ref AWS::StackName
```

---

## 3. Event-Driven Architecture Patterns

### Event Processing Paradigms

#### Synchronous Event Processing
```python
# For API Gateway events - synchronous response required
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.parser import event_parser
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
import json

app = APIGatewayRestResolver()

@app.get("/health")
@tracer.capture_method
def health_check():
    return {"statusCode": 200, "body": json.dumps({"status": "healthy"})}

@app.post("/api/endpoint")
@tracer.capture_method
def process_event(event: dict, context: LambdaContext) -> dict:
    try:
        # Process synchronous event
        result = EventProcessor(event).process()

        # Return immediate response
        return {
            "statusCode": 200,
            "body": json.dumps(result),
            "headers": {
                "Content-Type": "application/json",
                "X-Request-ID": context.aws_request_id
            }
        }
    except Exception as e:
        logger.exception("Failed to process synchronous event")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"}),
            "headers": {"Content-Type": "application/json"}
        }
```

#### Asynchronous Event Processing
```python
# For SQS/SNS events - can process asynchronously
from aws_lambda_powertools.utilities.parser import parse
from aws_lambda_powertools.utilities.typing import LambdaContext
import asyncio

@tracer.capture_method
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    """Handle asynchronous events with proper acknowledgment"""

    # Batch processing for SQS
    if 'Records' in event:
        results = []
        for record in event['Records']:
            try:
                # Process each message
                result = MessageProcessor(process_with_dlq_retry).process(record)
                results.append(result)
            except Exception as e:
                logger.error(f"Failed to process message {record['messageId']}: {str(e)}")
                # Partial batch failure - Lambda will retry

        return {
            "batchItemFailures": [
                {"itemIdentifier": record['messageId']}
                for record, success in zip(event['Records'], results)
                if not success
            ]
        }

    # Single event processing
    try:
        EventProcessor(event).process()
        return {"statusCode": 200}
    except Exception as e:
        logger.exception("Failed to process event")
        raise  # Trigger retry or DLQ
```

### Event Source Mappings

#### Standard SQS Event Source Mapping
```yaml
EventSourceMapping:
  Type: AWS::Lambda::EventSourceMapping
  Properties:
    BatchSize: 10
    Enabled: true
    EventSourceArn: !GetAtt MyQueue.Arn
    FunctionName: !GetAtt EventProcessorFunction.Arn
    FunctionResponseTypes:
      - ReportBatchItemFailures
    MaximumBatchingWindowInSeconds: 30
    ScalingConfig:
      MaximumConcurrency: 10
```

#### Kinesis Stream Processing
```yaml
KinesisEventSource:
  Type: AWS::Lambda::EventSourceMapping
  Properties:
    BatchSize: 100
    Enabled: true
    EventSourceArn: !GetAtt MyStream.Arn
    FunctionName: !GetAtt StreamProcessorFunction.Arn
    StartingPosition: TRIM_HORIZON
    TumblingWindowInSeconds: 300  # Enable tumbling windows
```

### Event Processing Patterns

#### Event Filtering and Routing
```python
class EventRouter:
    """Route events based on type and content"""

    @tracer.capture_method
    def route_event(self, event: dict) -> None:
        event_type = event.get('eventType', 'unknown')

        routes = {
            'ORDER_PLACED': self.process_order,
            'PAYMENT_RECEIVED': self.process_payment,
            'USER_REGISTERED': self.process_registration
        }

        handler = routes.get(event_type, self.process_unknown_event)
        handler(event)

    @tracer.capture_method
    def process_order(self, event: dict) -> None:
        """Process order events"""
        logger.info(f"Processing order: {event['orderId']}")
        # Implementation...

    @tracer.capture_method
    def process_payment(self, event: dict) -> None:
        """Process payment events"""
        logger.info(f"Processing payment: {event['paymentId']}")
        # Implementation...
```

---

## 4. CloudFormation/Serverless Framework Conventions

### CloudFormation Template Structure

#### Standard Template Organization
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: Lambda function stack with supporting resources

Parameters:
  Environment:
    Type: String
    Default: 'Development'
    AllowedValues: ['Development', 'Staging', 'Production']

Mappings:
  EnvironmentConfig:
    Development:
     dFunctionConcurrentExecutions: '10'
      MaxFunctionTimeout: '900'
    Production:
      MaxFunctionConcurrentExecutions: '100'
      MaxFunctionTimeout: '300'

Resources:
  # Lambda Execution Role
  LambdaExecutionRole:
    Type: AWS::IAM::Role
    Properties: # IAM configuration...

  # Lambda Function
  LambdaFunction:
    Type: AWS::Lambda::Function
    Properties: # Function configuration...

  # Supporting Resources
  # - Event Source Mappings
  # - API Gateway
  # - Dead Letter Queue
  # - CloudWatch Alarms
  # - Resource-based Policies

Outputs:
  FunctionArn:
    Description: Lambda function ARN
    Value: !GetAtt LambdaFunction.Arn
    Export:
      Name: !Sub "${Environment}-${AWS::StackName}-FunctionArn"
```

### Project-Specific CloudFormation Patterns

#### Reusable Lambda Function Template
```yaml
# lambda-function-template.yaml
Parameters:
  FunctionName:
    Type: String
  Runtime:
    Type: String
    Default: 'python3.12'
  MemorySize:
    Type: String
    Default: '256'
  Handler:
    Type: String
    Default: 'lambda_function.handler'

Resources:
  LambdaFunction:
    Type: AWS::Lambda::Function
    Properties:
      FunctionName: !Sub "${Environment}-${FunctionName}"
      Runtime: !Ref Runtime
      MemorySize: !Ref MemorySize
      Handler: !Ref Handler
      Code:
        S3Bucket: !Sub "${ArtifactBucket}"
        S3Key: !Sub "${ApplicationName}/${Environment}/functions/${FunctionName}.zip"
      Role: !GetAtt LambdaExecutionRole.Arn
      # Plus standard properties...

  LambdaLogGroup:
    Type: AWS::Logs::LogGroup
    Properties:
      LogGroupName: !Sub "/aws/lambda/${Environment}-${FunctionName}"
      RetentionInDays: !FindInMap [EnvironmentConfig, !Ref Environment, LogRetention]

  LambdaErrorsAlarm:
    Type: AWS::CloudWatch::Alarm
    Properties:
      AlarmName: !Sub "${Environment}-${FunctionName}-Errors"
      # Alarm configuration...
```

#### Lambda Layer Management
```yaml
LambdaLayers:
  PowerToolsLayer:
    Type: AWS::Lambda::LayerVersion
    Properties:
      LayerName: !Sub "${Environment}-lambda-powertools"
      Description: "AWS Lambda Powertools for Python"
      Content:
        S3Bucket: !Ref ArtifactBucket
        S3Key: !Sub "layers/powertools/${PowerToolsVersion}.zip"
      CompatibleRuntimes:
        - python3.9
        - python3.10
        - python3.11
        - python3.12

  SharedLibrariesLayer:
    Type: AWS::Lambda::LayerVersion
    Properties:
      LayerName: !Sub "${Environment}-shared-libraries"
      Description: "Shared libraries for all Lambda functions"
      Content:
        S3Bucket: !Ref ArtifactBucket
        S3Key: !Sub "layers/shared-libraries/${SharedLibrariesVersion}.zip"
      CompatibleRuntimes:
        - python3.12
```

---

## 5. API Gateway Integration Patterns

### REST API Integration

#### Path-Based Routing Pattern
```yaml
ApiGatewayRestApi:
  Type: AWS::ApiGateway::RestApi
  Properties:
    Name: !Sub "${Environment}-api-gateway"
    Description: "API Gateway for Lambda functions"
    EndpointConfiguration:
      Types:
        - REGIONAL

  ApiRootResource:
    Type: AWS::ApiGateway::Resource
    Properties:
      RestApiId: !Ref ApiGatewayRestApi
      ParentId: !GetAtt ApiGatewayRestApi.RootResourceId
      PathPart: 'api'

  # API Methods
  HealthMethod:
    Type: AWS::ApiGateway::Method
    Properties:
      RestApiId: !Ref ApiGatewayRestApi
      ResourceId: !GetAtt ApiRootResource
      HttpMethod: GET
      AuthorizationType: NONE
      Integration:
        Type: AWS_PROXY
        IntegrationHttpMethod: POST
        Uri: !Sub "arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${HealthFunction.Arn}/invocations"

  # API Deployment
  ApiGatewayDeployment:
    Type: AWS::ApiGateway::Deployment
    DependsOn: HealthMethod
    Properties:
      RestApiId: !Ref ApiGatewayRestApi
      StageName: !Ref Environment

  # Lambda Permissions
  ApiGatewayLambdaPermission:
    Type: AWS::Lambda::Permission
    Properties:
      FunctionName: !GetAtt HealthFunction.Arn
      Action: lambda:InvokeFunction
      Principal: apigateway.amazonaws.com
      SourceArn: !Sub "arn:aws:execute-api:${AWS::Region}:${AWS::AccountId}:${ApiGatewayRestApi}/*/*/*"
```

#### HTTP API Integration
```yaml
ApiGatewayV2HttpApi:
  Type: AWS::ApiGatewayV2::Api
  Properties:
    Name: !Sub "${Environment}-http-api"
    ProtocolType: HTTP
    CorsConfiguration:
      AllowCredentials: false
      AllowHeaders: ["*"]
      AllowMethods: ["*"]
      AllowOrigins: ["*"]
      ExposeHeaders: ["date", "keep-alive"]
      MaxAge: 86400

  ApiStage:
    Type: AWS::ApiGatewayV2::Stage
    Properties:
      ApiId: !Ref ApiGatewayV2HttpApi
      DeploymentId: !Ref ApiDeployment
      StageName: !Ref Environment

  ApiDeployment:
    Type: AWS::ApiGatewayV2::Deployment
    Properties:
      ApiId: !Ref ApiGatewayV2HttpApi

  # Lambda Integration
  HealthIntegration:
    Type: AWS::ApiGatewayV2::Integration
    Properties:
      ApiId: !Ref ApiGatewayV2HttpApi
      IntegrationType: AWS_PROXY
      IntegrationUri: !Sub "arn:aws:apigateway:${AWS::Region}:lambda:path/2015-03-31/functions/${HealthFunction.Arn}/invocations"
      PayloadFormatVersion: '2.0'

  # Route and Method
  HealthRoute:
    Type: AWS::ApiGatewayV2::Route
    Properties:
      ApiId: !Ref ApiGatewayV2HttpApi
      RouteKey: 'GET /api/health'
      Target: !Sub "integrations/${HealthIntegration}"
```

### Lambda API Integration Handler Pattern

#### Powertools Lambda Handler
```python
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.event_handler import APIGatewayRestResolver
from aws_lambda_powertools.utilities.parser import parse
from aws_lambda_powertools.utilities.validation import validate
import json
import os

app = APIGatewayRestResolver(
    cors=APIGatewayCorsConfig(
        allow_credentials=True,
        allow_headers=["Authorization", "Content-Type"],
        allow_methods=["GET", "POST"],
        allow_origin=["https://app.aigency.dev"],
        max_age=3600
    )
)

@app.get("/health")
@tracer.capture_method
def health_check():
    return {
        "statusCode": 200,
        "body": json.dumps({
            "status": "healthy",
            "service": os.getenv("POWERTOOLS_SERVICE_NAME"),
            "environment": os.getenv("ENVIRONMENT")
        })
    }

@app.post("/api/process")
@tracer.capture_method
@validate()
def process_api_request(event: APIGatewayProxyEventV2, context: LambdaContext):
    try:
        # Parse and validate request
        request_body = json.loads(event['body'] or '{}')

        # Process request
        result = ApiProcessor(request_body).process()

        return {
            "statusCode": 200,
            "body": json.dumps({
                "success": True,
                "data": result,
                "requestId": context.aws_request_id
            }),
            "headers": {
                "Content-Type": "application/json"
            }
        }

    except ValidationError as e:
        return {
            "statusCode": 400,
            "body": json.dumps({"error": "Validation failed", "details": str(e)}),
            "headers": {"Content-Type": "application/json"}
        }
    except Exception as e:
        logger.exception("Unexpected error in API processing")
        return {
            "statusCode": 500,
            "body": json.dumps({"error": "Internal server error"}),
            "headers": {"Content-Type": "application/json"}
        }

@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    return app.resolve(event, context)
```

---

## 6. Error Handling and Logging Best Practices

### Comprehensive Error Handling Pattern

#### Structured Error Handling
```python
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools import Logger, Tracer
import traceback
import json

logger = Logger()
tracer = Tracer()

class LambdaException(Exception):
    """Base exception for Lambda-specific errors"""
    def __init__(self, message: str, status_code: int = 500, details: dict = None):
        super().__init__(message)
        self.message = message
        self.status_code = status_code
        self.details = details or {}

class ValidationException(LambdaException):
    """Validation-related errors"""
    def __init__(self, message: str, field: str = None):
        super().__init__(message, status_code=400, details={"field": field})

class ResourceNotFoundException(LambdaException):
    """Resource not found errors"""
    def __init__(self, resource_type: str, resource_id: str):
        super().__init__(
            f"{resource_type} not found: {resource_id}",
            status_code=404,
            details={"resource_type": resource_type, "resource_id": resource_id}
        )

class ErrorHandler:
    @staticmethod
    @tracer.capture_method
    def handle_error(error: Exception, context: LambdaContext) -> dict:
        """
        Centralized error handling for Lambda functions

        Returns a properly formatted error response and logs the error
        """
        error_id = context.aws_request_id

        if isinstance(error, LambdaException):
            # Custom application errors
            logger.warning(
                f"Application error: {error.message}",
                extra={
                    "error_type": error.__class__.__name__,
                    "status_code": error.status_code,
                    "details": error.details,
                    "request_id": error_id
                }
            )

            return {
                "statusCode": error.status_code,
                "body": json.dumps({
                    "error": error.message,
                    "details": error.details,
                    "requestId": error_id
                }),
                "headers": {"Content-Type": "application/json"}
            }

        else:
            # Unexpected errors
            logger.exception(
                f"Unexpected error: {str(error)}",
                extra={
                    "error_type": error.__class__.__name__,
                    "traceback": traceback.format_exc(),
                    "request_id": error_id
                }
            )

            return {
                "statusCode": 500,
                "body": json.dumps({
                    "error": "Internal server error",
                    "requestId": error_id
                }),
                "headers": {"Content-Type": "application/json"}
            }
```

### Logging Strategy

#### Structured Logging Patterns
```python
from aws_lambda_powertools import Logger
from aws_lambda_powertools.logging import utils
import os

# Configure logger with standardized format
logger = Logger(
    service=os.getenv("POWERTOOLS_SERVICE_NAME", "unknown-service"),
    level=os.getenv("LOG_LEVEL", "INFO"),
    format="%(asctime)s %(levelname)s %(name)s %(funcName)s %(lineno)d %(message)s"
)

class StructuredLogger:
    """Structured logging utility for consistent log format"""

    @staticmethod
    def log_event_processing(event: dict, context: LambdaContext):
        """Log event processing start"""
        logger.info(
            "Processing event",
            extra={
                "event_type": StructuredLogger._get_event_type(event),
                "event_size": len(json.dumps(event)),
                "request_id": context.aws_request_id,
                "remaining_time": context.get_remaining_time_in_millis()
            }
        )

    @staticmethod
    def log_success(metric_name: str, duration_ms: int = None):
        """Log successful operation"""
        logger.info(
            f"Operation completed successfully",
            extra={
                "metric_name": metric_name,
                "duration_ms": duration_ms,
                "status": "success"
            }
        )

    @staticmethod
    def log_business_event(event_type: str, **kwargs):
        """Log business-specific events"""
        logger.info(
            f"Business event: {event_type}",
            extra={
                "event_type": "business",
                "business_event": event_type,
                **kwargs
            }
        )

    @staticmethod
    def _get_event_type(event: dict) -> str:
        """Determine event type for logging"""
        if 'Records' in event:
            if event['Records'][0].get('eventSource') == 'aws:sqs':
                return 'SQS_MESSAGE'
            elif event['Records'][0].get('eventSourceARN', '').startswith('arn:aws:kinesis:'):
                return 'KINESIS_RECORD'
            else:
                return 'SQS_COMPATIBLE'

        if 'requestContext' in event:
            return 'API_GATEWAY'

        if 'source' in event:
            return event['source'].upper()

        return 'UNKNOWN'
```

### Comprehensive Lambda Handler Template

#### Full Handler Implementation
```python
from aws_lambda_powertools import Logger, Tracer, Metrics
from aws_lambda_powertools.utilities.typing import LambdaContext
from aws_lambda_powertools.utilities.parser import parse
import json
import time

logger = Logger()
tracer = Tracer()
metrics = Metrics()

@metrics.log_metrics
@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext) -> dict:
    """
    Comprehensive Lambda handler with all best practices

    Args:
        event: AWS Lambda event
        context: AWS Lambda context

    Returns:
        dict: Response for synchronous calls, None for asynchronous
    """
    start_time = time.time()

    try:
        # Log event processing start
        StructuredLogger.log_event_processing(event, context)

        # Parse event based on type
        if _is_api_gateway_event(event):
            response = handle_api_gateway_event(event, context)
        elif _is_sqs_event(event):
            response = handle_sqs_event(event, context)
        elif _is_scheduled_event(event):
            response = handle_scheduled_event(event, context)
        else:
            logger.warning(f"Unknown event type", extra={"event_keys": list(event.keys())})
            response = {"statusCode": 400, "body": json.dumps({"error": "Unknown event type"})}

        # Log success
        duration = int((time.time() - start_time) * 1000)
        StructuredLogger.log_success("lambda_execution", duration)

        return response

    except Exception as e:
        # Centralized error handling
        duration = int((time.time() - start_time) * 1000)
        logger.error(
            f"Lambda execution failed: {str(e)}",
            extra={
                "duration_ms": duration,
                "exception_type": type(e).__name__
            }
        )

        # Return error response or raise to trigger retry/DLQ
        if _expects_response(event):
            return ErrorHandler.handle_error(e, context)
        else:
            raise

def _is_api_gateway_event(event: dict) -> bool:
    """Check if event is from API Gateway"""
    return 'requestContext' in event or 'body' in event

def _is_sqs_event(event: dict) -> bool:
    """Check if event is from SQS"""
    return 'Records' in event and event['Records'][0].get('eventSource') == 'aws:sqs'

def _is_scheduled_event(event: dict) -> bool:
    """Check if event is from EventBridge scheduler"""
    return event.get('source') == 'aws.events'

def _expects_response(event: dict) -> bool:
    """Check if caller expects a response"""
    return 'requestContext' in event or 'body' in event

def handle_api_gateway_event(event: dict, context: LambdaContext) -> dict:
    """Handle API Gateway events"""
    # Implementation as shown in Section 5
    pass

def handle_sqs_event(event: dict, context: LambdaContext) -> dict:
    """Handle SQS events"""
    # Implementation as shown in Section 3
    pass

def handle_scheduled_event(event: dict, context: LambdaContext) -> dict:
    """Handle scheduled events"""
    # Implementation for cron-like events
    pass
```

---

## Conclusion

This AGENTS.md documentation provides a comprehensive framework for AWS Lambda function development within the AI Agency project. The patterns and conventions outlined here ensure:

1. **Consistency** across all Lambda functions in the project
2. **Security** through proper secrets management and IAM practices
3. **Observability** through structured logging and monitoring
4. **Maintainability** through standardized packaging and deployment
5. **Scalability** through proper event-driven architecture patterns
6. **Cost Optimization** through resource configuration best practices

The patterns incorporate project-specific conventions that deviate from standard AWS practices where necessary for operational excellence, security compliance, and performance requirements.

---

## Appendix A: Quick Reference

### Lambda Configuration Checklist

- [ ] Function name follows naming convention: `${Environment}-${ServiceName}`
- [ ] Memory size starts at 256MB and scales as needed
- [ ] Timeout set to reasonable value (≤300 seconds for production)
- [ ] Concurrent executions limited to prevent runaway costs
- [ ] VPC configuration with private subnets
- [ ] Dead Letter Queue configured for failed events
- [ ] CloudWatch integration enabled for tracing
- [ ] Environment variables using secure parameter patterns
- [ ] Required Lambda layers attached
- [ ] Proper exception handling implemented
- [ ] Structured logging with Powertools
- [ ] Monitoring alarms configured

### Environment Variable Standards

| Variable | Purpose | Required | Security |
|----------|---------|----------|----------|
| `LOG_LEVEL` | Logging verbosity | Optional | Config |
| `TIMEOUT_SECONDS` | Function timeout | Optional | Config |
| `RETRY_ATTEMPTS` | Retry count | Optional | Config |
| `DB_HOST` | Database host | As needed | Config |
| `DB_PASSWORD` | Database password | Never | Retrieve via SSM |

### Common Function Patterns

1. **API Handler**: Synchronous response with proper HTTP status codes
2. **Event Processor**: Asynchronous processing with batch handling
3. **Scheduled Task**: Cron-like execution with Circuit Breaker pattern
4. **Webhook Handler**: Validation and idempotency with retry logic
5. **Stream Processor**: State management with checkpoint handling

---

## Appendix B: Migration Guide

### Migrating from Standard AWS Lambda Patterns

**From Basic Handler:**
```python
def lambda_handler(event, context):  # Old style
    return {"statusCode": 200, "body": "OK"}
```

**To Project Standard:**
```python
@metrics.log_metrics
@logger.inject_lambda_context
@tracer.capture_lambda_handler
def lambda_handler(event: dict, context: LambdaContext) -> dict:  # New style
    try:
        # Processing logic with proper error handling
        StructuredLogger.log_event_processing(event, context)
        return {"statusCode": 200, "body": json.dumps({"status": "success"})}
    except Exception as e:
        return ErrorHandler.handle_error(e, context)
```

**Key Improvements:**
- Type hints for better IDE support
- Structured logging with Powertools
- Comprehensive error handling
- Metrics collection
- Tracing support
- Consistent response format

---

*This documentation is maintained by the cloud-aws mode agents and should be updated when new patterns or best practices are established. For questions or contributions, please engage with the [cloud-aws architecture team](../../.ruru/modes/cloud-aws/kb/).*