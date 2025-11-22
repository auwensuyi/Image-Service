import boto3
import os
from botocore.exceptions import NoCredentialsError


class S3Service:
    def __init__(self):
        self.bucket = os.getenv("S3_BUCKET_NAME")
        self.region = os.getenv("AWS_REGION")

        self.client = boto3.client(
            "s3",
            aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
            aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
            region_name=self.region
        )

    def upload_file(self, file):
        """Upload a file-like object to S3 and return the URL"""
        try:
            filename = file.filename
            self.client.upload_fileobj(file, self.bucket, filename)

            return f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{filename}"

        except NoCredentialsError:
            raise Exception("AWS credentials missing or invalid")

        except Exception as e:
            raise Exception(f"S3 upload failed: {e}")
