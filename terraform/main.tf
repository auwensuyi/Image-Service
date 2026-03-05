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
  bucket = "my-unique-terraform-bucket-name-based-god" # Must be globally unique
  tags = {
    Project = "Terraform AWS Connection Demo"
  }
}
