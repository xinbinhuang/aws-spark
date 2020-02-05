# Apache Spark

This repo is a personal study effort for learning Spark for running jobs both locally and on AWS EMR.

## Dependency

Install `pipenv`

```bash
pip install pipenv
```

Install project deps

```bash
pipenv install --dev .
```

## AWS Setup

The above step would install aws cli in the virtualenv, but you can also install it globally.

```bash
pip install awscli

# you many also want to install the interative awsshell
# pip install awsshell
```

Then configure your credentials and default region with `aws configure`. The credential should have both programmatic and console access.

## Submit the book review job

First create S3 buckets for storing artifacts

```bash
export LOGS_BUCKET=s3://<bucket-for-logs>
export OUTPUTS_BUCKET=s3://<bucket-for-scripts>
export SCRIPTS_BUCKET=s3://<bucket-for-outputs>

aws s3 mb $LOGS_BUCKET
aws s3 mb $OUTPUTS_BUCKET
aws s3 mb $SCRIPTS_BUCKET

# upload script to the bucket
aws s3 cp ./src/book_review_pyspark_job.py $SCRIPTS_BUCKET
```

Create EC2 key-pairs

```bash
export KEY_PAIR=<key-name>
aws ec2 create-key-pair --key-name $KEY_PAIR > ~/.ssh/$KEY_PAIR.pem
```

Submit job to EMR

```bash
# create default role if you have not
# aws emr create-default-roles

# submit job
aws emr create-cluster --name "Book review spark cluster job" \
    --release-label emr-5.24.1 \
    --applications Name=Spark \
    --log-uri $LOGS_BUCKET \
    --ec2-attributes KeyName=$KEY_PAIR \
    --instance-type m5.xlarge \
    --instance-count 2 \
    --configurations file://./emr_spark_py3_conf.json \
    --steps Type=Spark,Name="Book Review Job",ActionOnFailure=CONTINUE,Args=[--deploy-mode,cluster,--master,yarn,$SCRIPTS_BUCKET/book_review_pyspark_job.py,$SCRIPTS_BUCKET] \
    --use-default-roles \
    --auto-terminate
```

## Run tests

```bash
pytest tests/
```

### Linting

```bash
# Autoformat
black .

# Check with Flake8
flake8 .
```

## TODO

- Add Cloudformation to set up resources for S3
- Scripts/docs for submitting jobs on EMR
- More examples
- More unit testing

