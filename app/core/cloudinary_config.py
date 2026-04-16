import cloudinary
from dotenv import load_dotenv
import os

load_dotenv()
cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_NAME"),
    api_key=os.getenv("CLOUDINARY_API"),
    api_secret=os.getenv("CLOUDINARY_SECRET_KEY")
)