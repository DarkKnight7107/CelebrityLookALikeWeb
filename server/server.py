from flask import Flask, request, jsonify, send_file
from PIL import Image
from flask_cors import CORS
import os

import face_recognition
import numpy as np

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
PROCESSED_FOLDER = os.path.join(BASE_DIR, "processed")
IMAGE_FOLDER = os.path.join(BASE_DIR, "images")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(PROCESSED_FOLDER, exist_ok=True)

known_encodings = []
known_images = []

def calculate_face_distance(known_images, known_encodings, unknown_img_path, cutoff=0.5, num_result=4):
    image_to_test = face_recognition.load_image_file(unknown_img_path)
    image_to_test_encoding = face_recognition.face_encodings(image_to_test)[0]
    encodings = face_recognition.face_encodings(image_to_test)
    if len(encodings) == 0:
        return jsonify({"error": "No face detected in the uploaded image"}), 400
    image_to_test_encoding = encodings[0]

    face_distances = face_recognition.face_distance(known_encodings, image_to_test_encoding)
    return (unknown_img_path, known_images[face_distances.argmin()])

def loadEncodings():
    encs = []
    actors = []
    with open(os.path.join(BASE_DIR, "encodings.txt"),'r') as fh:
        lines = fh.readlines()
        for line in lines:
            encs.append(np.array([float(num) for num in line.split()]))
    
    with open(os.path.join(BASE_DIR, "actors.txt"), 'r') as fh:
        lines = fh.readlines()
        for line in lines:
            actors.append(line[0:-1])
        
    return (encs, actors)


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

    # Load known encodings
    known_encodings, known_images = loadEncodings()
    if not known_encodings or not known_images:
        return jsonify({"error": "Celebrity database is empty"}), 500

    # Perform face recognition
    try:
        matching_image = calculate_face_distance(known_images, known_encodings, upload_path)[1]
    except IndexError:
        return jsonify({"error": "No face detected in the uploaded image"}), 400

    return jsonify({"image_url": f"http://localhost:5000/images/{matching_image}"})

@app.route("/images/<filename>")
def get_processed_image(filename):
    """Serve the processed image to the frontend"""
    file_path = os.path.join(IMAGE_FOLDER, filename)
    if os.path.exists(file_path):
        return send_file(file_path, mimetype="image/jpeg")
    return jsonify({"error": "File not found"}), 404

if __name__ == "__main__":
    app.run(debug=True)
