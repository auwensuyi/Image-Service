from flask import Flask, request, jsonify
from service import S3Service

s3_service = S3Service()
app = Flask(__name__)

items = ["Ajinboye", "Adedayo", "Uwensuyi"]

@app.route("/")
def index():
    return jsonify({"items": items})

@app.route("/upload", methods=["POST"])
def upload():
    if "file" not in request.files:
        return jsonify({"error": "No file part"}), 400

    file = request.files["file"]

    if file.filename == "":
        return jsonify({"error": "No filename"}), 400

    try:
        url = s3_service.upload_file(file)
        return jsonify({
            "message": "File uploaded successfully",
            "url": url
        }), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, threaded=True, debug=True)

