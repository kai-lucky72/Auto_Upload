import os
import time
import subprocess
import shutil

# Configuration
WATCH_FOLDER = r""  # Change this to the actual folder path
UPLOADED_FOLDER = os.path.join(WATCH_FOLDER, "uploaded")
UPLOAD_URL = "https://projects.benax.rw/f/o/r/e/a/c/h/p/r/o/j/e/c/t/s/4e8d42b606f70fa9d39741a93ed0356c/iot_testing_202501/upload.php"

# Ensure uploaded folder exists
os.makedirs(UPLOADED_FOLDER, exist_ok=True)

def upload_image(image_path):
    """Uploads an image using curl and returns success or failure."""
    try:
        command = f'curl -X POST -F imageFile=@{image_path} {UPLOAD_URL}'
        result = subprocess.run(command, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Uploaded: {image_path}")
            return True
        else:
            print(f"Failed to upload: {image_path}, Error: {result.stderr}")
            return False
    except Exception as e:
        print(f"Error uploading {image_path}: {e}")
        return False

def monitor_folder():
    """Continuously checks for new images and uploads them."""
    print(f"Monitoring folder: {WATCH_FOLDER}")
    while True:
        for filename in os.listdir(WATCH_FOLDER):
            file_path = os.path.join(WATCH_FOLDER, filename)

            # Check if it's a valid image file
            if os.path.isfile(file_path) and filename.lower().endswith(('.jpg', '.jpeg', '.png')):
                if upload_image(file_path):
                    shutil.move(file_path, os.path.join(UPLOADED_FOLDER, filename))

        time.sleep(30)  # Wait for 30 seconds before checking again

if __name__ == "__main__":
    monitor_folder()
