Online Ledger
=============

Launching localstack with some logging:

> DEBUG=1 docker-compose up

Cloudformation deployment:
```
aws  --endpoint-url=http://localhost:4581 \
    cloudformation create-stack \
    --stack-name ledger-stack \
    --template-body file://deployment.yml \
    --parameters "ParameterKey=Region,ParameterValue=us-east-1"

```

Or manually: initial call for function creation:
```
aws  --endpoint-url=http://localhost:4574 \
    lambda create-function \
    --function-name sample \
    --code S3Bucket="__local__",S3Key="/opt/lambda" \
    --handler basic.handler  \
    --runtime python3 \
    --role localrole
```

Function call:
```
aws  --endpoint-url=http://localhost:4574 \
    lambda invoke \
    --function-name sample \
    --payload '{"input": "dummy"}' output
```

Code changes are manually activated:
```
aws  --endpoint-url=http://localhost:4574 \
    lambda update-function-code \
    --function-name sample \
    --s3-bucket "__local__" \
    --s3-key "/opt/lambda"
```

Listing S3 buckets:
```
aws  --endpoint-url=http://localhost:4572 \
    s3 ls
```
