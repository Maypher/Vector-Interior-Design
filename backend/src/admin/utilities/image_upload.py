import aiofiles
import uuid
import cloudinary.uploader
from sanic.request import File
import cloudinary
from common.utils import read_secret
from os import environ
from admin.utilities import file_extension

STORAGE_LOCATION = "/storage/images/"


async def upload_locally(image: File) -> str:
    """Saves an image locally and returns its filename"""
    file_ext = file_extension(image.name)

    image_name = uuid.uuid4().hex
    image_filename = f"{image_name}{file_ext}"
    image_location = f"{STORAGE_LOCATION}{image_filename}"

    async with aiofiles.open(image_location, "wb") as file:
        await file.write(image.body)

    return image_filename


cloudinary.config(
    cloud_name=environ.get("CLOUDINARY_NAME"),
    api_key=environ.get("CLOUDINARY_PUBLIC_KEY"),
    api_secret=read_secret("cloudinary_private_key"),
    secure=True,
)


def upload_to_cdn(image: File) -> str:
    """Uploads an image to the cdn and returns it's uuid"""
    uploaded_file = cloudinary.uploader.upload(
        image.body, quality="auto", format="jpeg"
    )

    return uploaded_file["public_id"]


def delete_from_cdn(image_id: str) -> bool:
    res = cloudinary.uploader.destroy(image_id)["result"] == "ok"
    return res
