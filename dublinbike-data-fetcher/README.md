# dublinbike-datafetch

Includes:
* Periodically invoked lambda that fetches dublin bike status and posts it into S3.
* Program that fetches all S3 data and injects it into ES

dunblin bikes URL:
https://api.jcdecaux.com/vls/v1/stations?apiKey=0d6ab5aa64bce5f166c365c079f4e0fef0073fc8&contract=dublin

## Deploy

Requirements:
* serverless framework
* AWS credentials

to deploy, run:

```
sls deploy
```

## TODO

[] compress files. It will bring data reduction of 85%
[] define infra variables in separate file (bucket name...)
[] check tracing https://serverless.com/framework/docs/providers/aws/guide/functions#aws-x-ray-tracing