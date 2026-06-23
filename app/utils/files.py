import os
from uuid import uuid4

UPLOAD_DIR = "uploads"

os.makedirs(UPLOAD_DIR, exist_ok=True)


def save_image(file):
    ext = file.filename.split(".")[-1]
    filename = f"{uuid4()}.{ext}"
    path = os.path.join(UPLOAD_DIR, filename)

    with open(path, "wb") as buffer:
        buffer.write(file.file.read())

    return path