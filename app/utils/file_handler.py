import requests
import os
import uuid


def download_file_from_url(url):
    try:
        response = requests.get(url)

        if response.status_code != 200:
            raise Exception(f"Failed to download file from {url} - Status: {response.status_code}")

        # extract extension safely from URL
        path_without_query = url.split("?")[0]
        ext = os.path.splitext(path_without_query)[1]
        
        # fallback if extension is missing in URL
        if not ext:
            ext = ".pdf" # default to pdf if unknown
        elif not ext.startswith("."):
            ext = f".{ext}"

        filename = f"{uuid.uuid4()}{ext}"
        folder = "temp"

        os.makedirs(folder, exist_ok=True)

        file_path = os.path.join(folder, filename)

        with open(file_path, "wb") as f:
            f.write(response.content)

        return file_path

    except Exception as e:
        print(f"DOWNLOAD ERROR at URL {url}: {str(e)}")
        raise Exception(f"Download error: {str(e)}")