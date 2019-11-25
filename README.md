Online Ledger
=============

Launching the localstack set of services:

> DEBUG=1 docker-compose up

You get more detailed logging by setting the DEBUG environment variable.

Cloudformation deployment:
```
> aws  --endpoint-url=http://localhost:4581 \
    cloudformation create-stack \
    --stack-name ledger-stack \
    --template-body file://deployment.yml \
    --parameters "ParameterKey=Region,ParameterValue=us-east-1"

```

Function call:
```
> aws  --endpoint-url=http://localhost:4574 \
    lambda invoke \
    --function-name Sample \
    --payload '{"input": "dummy"}' output
```

Code changes are manually activated:
```
> aws  --endpoint-url=http://localhost:4574 \
    lambda update-function-code \
    --function-name Sample \
    --s3-bucket "__local__" \
    --s3-key "/opt/lambda"
```

Listing S3 buckets:
```
> aws  --endpoint-url=http://localhost:4572 s3 ls
```

Listing functions:
```
> aws  --endpoint-url=http://localhost:4574 lambda list-functions
```

Listing REST APIs:
```
> aws --endpoint-url=http://localhost:4567 cloudformation describe-stacks --stack-name ledger-stack --query Stacks[0].Outputs
> aws --endpoint-url=http://localhost:4567 apigateway get-resources --rest-api-id <ApiId>
```

Requests follow the pattern: http://localhost:4567/restapis/<ApiId>/<stage>/_user_request_/<path>
Example: http://localhost:4567/restapis/zzaztl3gqs/v1/_user_request_/entries
