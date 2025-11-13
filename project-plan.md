# 🖼️ Image Service

The **Image Service** manages image upload, retrieval, update, and deletion.  
Built with **Python (Flask)** and using **AWS S3** for storage. Infrastructure is managed with **Terraform** and CI/CD is handled via configurable pipelines.

---

## Table of Contents
- [Infrastructure (Terraform)](#infrastructure-terraform)
  - [S3 Bucket](#s3-bucket)
  - [IAM User / Role](#iam-user--role)
- [Application — Python Flask API](#application---python-flask-api)
  - [Overview](#overview)
  - [Endpoints](#endpoints)
  - [Example Folder Structure](#example-folder-structure)
  - [Notes / Best Practices](#notes--best-practices)
- [CI/CD Automation](#cicd-automation)
  - [Release Pipeline](#release-pipeline)
  - [Build Pipeline](#build-pipeline)
  - [PR Pipeline](#pr-pipeline)
- [Tech Stack](#tech-stack)
- [Example Workflow](#example-workflow)
- [Future Improvements](#future-improvements)
- [Author](#author)

---

## Infrastructure (Terraform)

### S3 Bucket

**Purpose:** Store user-uploaded images.  
**Implementation:** Defined in Terraform.

**Key configurations**
- Versioning enabled for rollback support.  
- Server-side encryption (SSE-S3 or SSE-KMS).  
- Public access blocked by default.  
- CORS configuration for Flask API access.  
- Lifecycle rules (optional) for archiving or auto-deletion.

**Example Terraform snippet**
```hcl
resource "aws_s3_bucket" "image_bucket" {
  bucket = "image-service-bucket"
  acl    = "private"

  versioning {
    enabled = true
  }

  server_side_encryption_configuration {
    rule {
      apply_server_side_encryption_by_default {
        sse_algorithm = "AES256"
      }
    }
  }

  tags = {
    Name = "image-service-bucket"
  }
}
```

---

### IAM User / Role

**Purpose:** Provide *least-privilege* access to the S3 bucket.  
**Implementation:** Managed via **Terraform**.

**Permissions**
- `s3:PutObject`  
- `s3:GetObject`  
- `s3:DeleteObject`  
- `s3:ListBucket`

**Attached Policy:** Custom IAM policy attached to a specific IAM user or service role.

**Example minimal policy (JSON)**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Action": [
        "s3:PutObject",
        "s3:GetObject",
        "s3:DeleteObject",
        "s3:ListBucket"
      ],
      "Resource": [
        "arn:aws:s3:::image-service-bucket",
        "arn:aws:s3:::image-service-bucket/*"
      ]
    }
  ]
}
```

---

## Application — Python Flask API

### Overview
A lightweight REST API for handling image uploads and retrievals. The Flask service generates **pre-signed URLs** for direct S3 interaction, which reduces server bandwidth and improves scalability.

### Endpoints

| Method  | Endpoint                   | Description                                 |
|--------:|----------------------------|---------------------------------------------|
| `POST`  | `/upload`                  | Upload an image to S3                       |
| `GET`   | `/image/<filename>`        | Retrieve an image from S3                   |
| `PUT`   | `/update/<filename>`       | Update or replace an existing image         |
| `DELETE`| `/delete/<filename>`       | Delete an image from S3                     |

**Notes about endpoints**
- `<filename>` is a path parameter; replace angle brackets with the actual file key when making requests.
- Use authentication (JWT, API key, or IAM-backed) for production APIs.
- Endpoints should return JSON responses with appropriate status codes.

### Example Folder Structure
```text
image-service/
├── app.py
├── requirements.txt
├── config.py
├── services/
│   └── s3_service.py
├── utils/
│   └── logger.py
├── tests/
│   └── test_api.py
├── Dockerfile
└── .github/
    └── workflows/
        └── ci.yml
```

### Example Flask route (upload)
```python
from flask import Flask, request, jsonify
from services.s3_service import upload_file

app = Flask(__name__)

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files.get('file')
    if not file:
        return jsonify({"error": "no file provided"}), 400

    key = upload_file(file)  # implements validation + upload
    return jsonify({"key": key}), 201
```

### Notes / Best Practices
- Validate file types and limit size before upload.  
- Use environment variables or secret managers for AWS credentials.  
- Implement rate limiting and authentication for production.  
- Add logging and monitoring for observability.

---

