Amazon S3 で Amazon Lambda を使用する
===================================

# 使用ツール

* [Serverless Framework](https://serverless.com/)

# Build

```
$ ./build.sh
```

# AWS Lambda-backed カスタムリソースのデプロイ

```
$ cd deploy/trigger
$ sls deploy -s [stage] -r [region] -v
```

# カスタムリソースを使って Lambda のデプロイ

```
$ cd deploy/consumer
$ BUCKET_NAME=[YOUR BUCKET NAME] sls deploy -s [stage] -r [region] -v
```

# 仕組み

Cloudformation のカスタムリソースの仕組みを使い、trigger.py では、s3 の [put_bucket_notification_configuration](https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html#S3.Client.put_bucket_notification_configuration) を実行して、Create, Update, Delete を行います。
Lambda の AddPermission は、別途 Cloudformation で追加する必要があります。
