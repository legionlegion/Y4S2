"""
client-side
watch a directory
send any new file to server
"""

import os
import time
import requests

import getpass
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

"""
for WSL users, download ngrok and pyngrok to enable public HTTP access from EC2 to WSL:
https://ngrok.com/downloads/linux 
pip install pyngrok
"""

from pyngrok import ngrok

http_tunnel = ngrok.connect(6000)
LOCAL_IP = http_tunnel.__dict__.get('public_url').removeprefix('https://')

WATCH_DIR = "/home/timothy/sampleML/raw_input"
EC2_API_URL = "http://ec2-13-215-59-34.ap-southeast-1.compute.amazonaws.com:5000/upload" # change to your own ec2 ipv4 later
OUTPUT_DIR = "/home/timothy/sampleML/output"
LOCAL_USER = getpass.getuser()
WATCH_INTERVAL = 1

class UploadHandler(FileSystemEventHandler):
    def on_created(self, event):
        if event.is_directory:
            return
        file_path = event.src_path
        file_name = os.path.basename(file_path)
        print(f"Detected new file: {file_name}")

        # send data as binary, the safest method
        with open(file_path, "rb") as f:
            files = {"file": (file_name, f)}
            data = {
                "username": LOCAL_USER,
                "client_ip": LOCAL_IP,
                "output_dir": OUTPUT_DIR
            }
            try:
                r = requests.post(EC2_API_URL, files=files, data=data)
                print(r.json())
            except Exception as e:
                print("Failed to upload:", e)

if __name__ == "__main__":
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    event_handler = UploadHandler()
    observer = Observer()
    observer.schedule(event_handler, WATCH_DIR, recursive=False)
    observer.start()
    print(f"Watching {WATCH_DIR} for new files...")

    try:
        while True:
            time.sleep(WATCH_INTERVAL)
    except KeyboardInterrupt:
        observer.stop()
        ngrok.kill()
    observer.join()
