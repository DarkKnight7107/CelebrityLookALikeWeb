from flask import Flask, request, jsonify, send_file
from PIL import Image
from flask_cors import CORS
import os

app = Flask(__name__)
CORS(app)

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

    # Save original uploaded image
    upload_path = os.path.join(UPLOAD_FOLDER, file.filename)
    file.save(upload_path)

    # Open the uploaded image and flip it
    image = Image.open(upload_path)
    flipped_image = image.transpose(Image.FLIP_TOP_BOTTOM)

    # Always save as 'person.jpg' in processed folder
    processed_filename = "person.jpg"
    processed_path = os.path.join(PROCESSED_FOLDER, processed_filename)
    flipped_image.save(processed_path)

    # Return fixed processed image URL
    return jsonify({"image_url": "http://localhost:5000/processed/person.jpg"})

@app.route("/processed/<filename>")
def get_processed_image(filename):
    """Serve the processed image to the frontend"""
    file_path = os.path.join(PROCESSED_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, mimetype="image/jpeg")
    return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
