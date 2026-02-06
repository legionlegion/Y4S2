"""
server-side
detects new file from client
run processing
send back to client
"""

from flask import Flask, request, jsonify
import os
import subprocess
import threading
import requests

app = Flask(__name__)
UPLOAD_DIR = "/home/ec2-user/uploads"
PROCESS_SCRIPT = "/home/ec2-user/ec2_model_inference.py"
MODEL_PATH = "/home/ec2-user/model.joblib"
OUTPUT_DIR = "/home/ec2-user/processed"
POST_PROCESS_APPENDAGE = "_processed"

# Make sure folders exist
os.makedirs(UPLOAD_DIR, exist_ok=True)
os.makedirs(OUTPUT_DIR, exist_ok=True)

def process_and_return(file_path, original_filename, username, client_ip):
    # Build output filename
    base_name = os.path.basename(file_path)
    output_file = os.path.join(OUTPUT_DIR, f"{base_name.removesuffix('.csv')}{POST_PROCESS_APPENDAGE}.csv")

    # Run processing script
    subprocess.run(["python3", PROCESS_SCRIPT, MODEL_PATH, file_path, output_file])

    # Send processed file back to client via HTTP POST
    url = f"http://{client_ip}/receive"
    with open(output_file, "rb") as f:
        files = {"file": (os.path.basename(output_file), f)}
        data = {"original_filename": original_filename}
        try:
            r = requests.post(url, files=files, data=data)
            print(f"Sent {output_file} back to {client_ip}, status {r.status_code}")
        except Exception as e:
            print("Failed to send file back:", e)

@app.route("/upload", methods=["POST"])
def upload_file():
    file = request.files.get("file")
    username = request.form.get("username")
    client_ip = request.form.get("client_ip")
    client_output_dir = request.form.get("output_dir")

    if not all([file, username, client_ip, client_output_dir]):
        return jsonify({"error": "Missing parameters"}), 400

    # Save uploaded file
    original_filename = file.filename
    filename = f"{username}@{client_ip}__{original_filename}"
    file_path = os.path.join(UPLOAD_DIR, filename)
    file.save(file_path)
    print(f"Saved {filename} from {username}@{client_ip}")

    # Process asynchronously to immediately inform client that file is received 
    threading.Thread(
        target=process_and_return,
        args=(file_path, original_filename, username, client_ip)
    ).start()

    return jsonify({"status": "ok", "filename": filename})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
