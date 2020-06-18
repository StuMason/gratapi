import os

from dotenv import load_dotenv


class Config:
    def __init__(self):
        load_dotenv()
        self.initialise_app()
        self.initialise_s3()

    def initialise_app(self):
        self.app_env = "local"
        if "APP_ENV" in os.environ:
            self.app_env = os.environ.get("APP_ENV")

        self.app_name = "gratapi"
        if "APP_NAME" in os.environ:
            self.app_name = os.environ.get("APP_NAME")

        self.app_region = "eu-west-1"
        if "APP_REGION" in os.environ:
            self.app_region = os.environ.get("APP_REGION")

        self.aws_key = None
        if "AwsKey" in os.environ:
            self.aws_key = os.environ.get("AwsKey")

        self.aws_secret = None
        if "AwsSecret" in os.environ:
            self.aws_secret = os.environ.get("AwsSecret")

        self.aws_region = "eu-west-1"
        if "AwsRegion" in os.environ:
            self.aws_region = os.environ.get("AwsRegion")

    def initialise_s3(self):
        self.s3_endpoint = None
        if "S3_ENDPOINT" in os.environ:
            self.s3_endpoint = os.environ.get("S3_ENDPOINT")
