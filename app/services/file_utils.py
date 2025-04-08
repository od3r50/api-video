import mimetypes
import requests
import os
from uuid import uuid4
import shutil
import tempfile

def download_file(url):
    temp_dir = tempfile.mkdtemp()

    r = requests.get(url, stream=True)
    content_type = r.headers.get("Content-Type", "")
    ext = mimetypes.guess_extension(content_type) or ".bin"

    file_name = os.path.join(temp_dir, f"tmp_{uuid4().hex}.{ext}")    

    with open(file_name, "wb") as f:
        for chunk in r.iter_content(chunk_size=8192):
            f.write(chunk)
    return file_name, temp_dir

def clean_temp_files(temp_dir):
    if isinstance(temp_dir, str) and os.path.exists(temp_dir):
        shutil.rmtree(temp_dir)