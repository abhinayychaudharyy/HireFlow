import cloudinary.uploader
import cloudinary.utils
from app.core.cloudinary_config import cloudinary


def upload_resume(file_obj, filename=None):
    """
    Uploads a file object to Cloudinary and returns a secure, signed URL.
    """

    # Use auto-detection but capture the actual type for signing
    upload_result = cloudinary.uploader.upload(
        file_obj,
        use_filename=True,
        unique_filename=True,
        resource_type="auto"
    )

    # Capture the actual resource type decided by Cloudinary (raw, image, etc.)
    # This is critical for generating a valid signature
    actual_resource_type = upload_result.get("resource_type", "auto")

    # Generate a signed URL using the CORRECT resource type
    signed_url, _ = cloudinary.utils.cloudinary_url(
        upload_result["public_id"],
        resource_type=actual_resource_type,
        secure=True,
        sign_url=True
    )

    return signed_url