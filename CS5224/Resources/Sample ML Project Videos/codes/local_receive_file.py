"""
client-side
host a flask app to receive output files from server
"""

from flask import Flask, request
import os
import shutil

app = Flask(__name__)
RAW_INPUT_DIR = "/home/timothy/sampleML/raw_input/"
OUTPUT_DIR = "/home/timothy/sampleML/output/"
PROCESSED_INPUT_DIR = "/home/timothy/sampleML/processed_input/"

os.makedirs(OUTPUT_DIR, exist_ok=True)

@app.route("/receive", methods=["POST"])
def receive_file():
    file = request.files.get("file")
    if not file:
        return {"error": "No file"}, 400

    file_path = os.path.join(OUTPUT_DIR, file.filename)
    file.save(file_path)
    print(f"Received processed file: {file.filename}")

    # move original input file to directory for processed inputs
    original_filename = request.form.get("original_filename")
    original_path = os.path.join(RAW_INPUT_DIR, original_filename)
    dest_path = os.path.join(PROCESSED_INPUT_DIR, original_filename)

    if os.path.exists(original_path):
        shutil.move(original_path, dest_path)
        print(f"Moved input file: {original_path} to {dest_path}")

    return {"status": "ok"}

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=6000)
