import os
from uuid import uuid4

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)

def save_image(file):
    ext = file.filename.split(".")[-1].lower()
    filename = f"{uuid4()}.{ext}"

    filepath = os.path.join(UPLOAD_DIR, filename)

    with open(filepath, "wb") as buffer:
        buffer.write(file.file.read())

    # Return the web-accessible path
    return f"/uploads/{filename}"
