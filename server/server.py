from flask import Flask, request, jsonify
from flask_cors import CORS
from script import complex_processing  # Import function from script.py

app = Flask(__name__)
CORS(app)  # Allow frontend to communicate with backend

@app.route('/process', methods=['POST'])
def process():
    data = request.json  # Get JSON input from frontend
    user_input = data.get("input")  # Extract input value

    # Call the function from script.py
    output_data = complex_processing(user_input)

    return jsonify(output_data)  # Return the result as JSON

if __name__ == '__main__':
    app.run(debug=True)
