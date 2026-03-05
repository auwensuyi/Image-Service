# 🖼️ Image Service

Testing some stuff with onehpee

A lightweight and efficient **Image Upload Service** built with **Python Flask**, designed to handle image uploads to **AWS S3 (Object Storage)**.  
The service returns both a **pre-signed URL** (for secure access) and the **S3 object location URL** upon successful upload.

---

## 🚀 Overview

This microservice provides a simple and secure REST API for handling image uploads.  
It’s ideal for projects where image management is required without tightly coupling storage logic to the main application.

### ✅ Core Features
- Upload images to **AWS S3** buckets.
- Automatically generate and return:
  - **Pre-signed URL** (temporary, secure access)
  - **S3 file location URL**
- Lightweight **Flask REST API**
- Environment-based configuration
- Ready for **containerization** and **deployment on AWS**

---

## 🧱 Tech Stack

| Component | Technology |
|------------|-------------|
| **Language** | Python 3.x |
| **Framework** | Flask |
| **Cloud Storage** | AWS S3 |
| **Deployment** | Docker / AWS ECS / Lambda (optional) |
| **Environment Management** | `.env` with `python-dotenv` |

---

## ⚙️ Architecture

```mermaid
flowchart TD
A[Client Request] --> B[Flask REST API]
B --> C[AWS SDK - boto3]
C --> D[(S3 Bucket)]
D --> E[Return JSON with presigned_url + s3_url]
