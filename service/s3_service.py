import boto3
import os
from botocore.exceptions import NoCredentialsError
from validations.file_validations import FileValidations


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
            if file is None:
                raise ValueError("No file provided")

            if file.filename == "":
                raise ValueError("File has no name")

            filename = file.filename

            # Extension + MIME validation
            if not FileValidations.validate(file):
                raise ValueError("Invalid image type")

            # Upload to S3
            self.client.upload_fileobj(file, self.bucket, filename)
            presigned_url = self.get_presigned_url(filename)
            return {
                "url": f"https://{self.bucket}.s3.{self.region}.amazonaws.com/{filename}",
                "presigned_url": presigned_url
            }


        except NoCredentialsError:
            raise RuntimeError("AWS credentials missing or invalid")

        except Exception as e:
            raise RuntimeError(f"S3 upload failed: {e}")

    def get_presigned_url(self, filename):
        """Generate presigned url for given filename."""
        try:
            return self.client.generate_presigned_url(
                ClientMethod="get_object",
                Params={"Bucket": self.bucket, "Key": filename},
                ExpiresIn=3600,
            )
        except Exception as e:
            raise RuntimeError(f"S3 presigned url failed: {e}")
