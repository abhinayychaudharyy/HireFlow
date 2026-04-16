import cloudinary.uploader
from app.core.cloudinary_config import cloudinary # Ensure config is loaded

def upload_resume(file_obj):
    """
    Uploads a file object to Cloudinary and returns the secure URL.
    """
    upload_result = cloudinary.uploader.upload(file_obj, folder="resumes")
    return upload_result.get("secure_url")
