import os
from datetime import datetime
UPLOAD_DIR = os.getenv("UPLOAD_DIR", "/data/uploads")   # <-- persistent disk
os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_uploaded_image(file):
    ts = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
    filename = f"{ts}_{file.filename}"
    path = os.path.join(UPLOAD_DIR, filename)
    with open(path, "wb") as f:
        f.write(file.file.read())
    return path
