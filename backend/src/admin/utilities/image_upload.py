import aiofiles
import uuid
import aiofiles.os
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


async def delete_locally(filename: str) -> bool:
    """Deletes the given image from system. Returns `True` if the image was found and deleted. Otherwise `False`."""
    location = f"{STORAGE_LOCATION}{filename}"
    if await aiofiles.os.path.exists(location):
        await aiofiles.os.remove(location)
        return True

    return False
