Online Ledger
=============

Launching the localstack set of services:

> DEBUG=1 docker-compose up

You get more detailed logging by setting the DEBUG environment variable.

We then deploy the infrastructure with Cloudformation:
```
> aws  --endpoint-url=http://localhost:4581 \
    cloudformation create-stack \
    --stack-name ledger-stack \
    --template-body file://deployment.yml \
    --parameters "ParameterKey=Region,ParameterValue=us-east-1"

```

This creates in particular the S3 bucket for the next stage, which is the `serverless` deployment of our lambda functions:

```
SLS_DEBUG=3 sls deploy --stage local --region us-east-1
```

Listing S3 buckets:
```
> aws  --endpoint-url=http://localhost:4572 s3 ls
```

Listing functions:
```
> aws  --endpoint-url=http://localhost:4574 lambda list-functions
```
