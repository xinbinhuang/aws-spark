# Apache Spark

## AWS Setup

### CLI tools

To install it globally

```bash
pip install awscli awsshell
```

Then configure your credentials and default region with `aws configure`. The credential should have both programmatic and console access.

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
