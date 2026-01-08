from flask import Flask, request, jsonify
from service.s3_service import S3Service

s3_service = S3Service()
app = Flask(__name__)

items = ["Ajinboye", "Adedayo", "Uwensuyi", "Mason", "Osaretin"]

@app.route("/")
def index():
    return jsonify({"items": items})

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    try:
        payload = s3_service.upload_file(request.files["file"])
        return jsonify({
            "message": "File uploaded successfully",
            "url": payload["url"],
            "presigned_url": payload["presigned_url"],
            "statusCode": 200
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@app.route('/delete-file/<filename>', methods=['DELETE'])
def delete(filename):
    if not filename:
        return jsonify({"error": "filename is required"}), 400
    success = s3_service.delete_file(filename)

    if success:
        return jsonify({"message": "File deleted successfully"}), 200
    else:
        return jsonify({"error": "Failed to delete file"}), 500
    




if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True, debug=True)

