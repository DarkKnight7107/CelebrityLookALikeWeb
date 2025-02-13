from flask import Flask, request, jsonify, send_file, url_for
from PIL import Image
import os

app = Flask(__name__)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
PROCESSED_FOLDER = os.path.join(BASE_DIR, "processed")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

@app.route("/upload", methods=["POST"])
def upload_file():
    if "image" not in request.files:
        return jsonify({"error": "No image provided"}), 400

    file = request.files["image"]

    if file.filename == "":
        return jsonify({"error": "No selected file"}), 400

    # Save the uploaded image
    file_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(file_path)

    # Process the image (Flip Vertically)
    image = Image.open(file_path)
    flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)

    # Save the processed image
    processed_filename = f"flipped_{file.filename}"
    processed_path = os.path.join(PROCESSED_FOLDER, processed_filename)
    flipped_image.save(processed_path)

    # Return the URL of the processed image
    return jsonify({"image_url": url_for('get_processed_image', filename=processed_filename, _external=True)})

@app.route("/processed/<filename>")
def get_processed_image(filename):
    return send_file(os.path.join(PROCESSED_FOLDER, filename), mimetype="image/jpeg")

if __name__ == "__main__":
    app.run(debug=True)
