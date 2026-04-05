terraform {
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0" # Use a specific version for stability
    }
  }
}

# Configure the AWS provider
provider "aws" {
  region = "us-east-1" # Specify your desired AWS region
}

# Example: Create an S3 bucket
resource "aws_s3_bucket" "example_bucket_test" {
  bucket = "testing-with-onehpee-and-mkultra-bucket" # Must be globally unique
  tags = {
    Project = "Terraform AWS Connection Demo"
  }
}

resource "aws_iam_user" "image-uploader" {
  name = "image-uploader-test"
  path = "/"

  tags = {
    tag-key = "tag-value"
  }
}

resource "aws_iam_access_key" "image-uploader-access-key" {
  user = aws_iam_user.image-uploader.name
}

data "aws_iam_policy_document" "image-uploader-ro" {
  statement {
    effect    = "Allow"
    actions   = ["s3:ListAllMyBuckets", "s3:GetBucketLocation", "s3:PutObject", "s3:GetObject", "s3:DeleteObject", "s3:ListBucket"]
    resources = [
      "*",
      "arn:aws:s3:::image-service-bucket-based",
      "arn:aws:s3:::image-service-bucket-based/*",
      "arn:aws:s3:::thumbnail-image-service",
      "arn:aws:s3:::thumbnail-image-service/*"
    ]
  }
}

resource "aws_iam_user_policy" "lb_ro" {
  name   = "testing-policy-with-onehpee-and-mkultra"
  user   = aws_iam_user.image-uploader.name
  policy = data.aws_iam_policy_document.image-uploader-ro.json
}
