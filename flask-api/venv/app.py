from flask import Flask, jsonify, request, redirect, url_for
import boto3, os
from botocore.exceptions import NoCredentialsError
from dotenv import load_dotenv

load_dotenv()

app = Flask(__name__)

# AWS S3 Configuration from environment variables
S3_BUCKET_NAME = os.getenv("S3_BUCKET_NAME")
AWS_REGION = os.getenv("AWS_REGION")

# Initialize S3 client
s3 = boto3.client(
    "s3",
    aws_access_key_id=os.getenv("AWS_ACCESS_KEY_ID"),
    aws_secret_access_key=os.getenv("AWS_SECRET_ACCESS_KEY"),
    region_name=AWS_REGION
)

items = [3,4,5]

@app.route('/', methods=['GET'])
def get_items():
    return jsonify({'/': items})

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return "No file part", 400
    file = request.files['file']
    if file.filename == '':
        return "No selected file", 400

    if file:
        try:
            filename = file.filename
            s3.upload_fileobj(file, S3_BUCKET_NAME, filename)
            # You can also generate a public URL for the uploaded file
            object_url = f"https://{S3_BUCKET_NAME}.s3.{AWS_REGION}.amazonaws.com/{filename}"
            return f"File uploaded successfully! View at: {object_url}"
        except NoCredentialsError:
            return "AWS credentials not found or invalid", 500
        except Exception as e:
            return f"Error uploading file: {e}", 500
    return "Something went wrong", 500

if __name__ == '__main__':
    app.run(debug=True)