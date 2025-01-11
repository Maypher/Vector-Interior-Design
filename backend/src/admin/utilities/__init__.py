import re

ALLOWED_EXTENSIONS = ["image/png", "image/jpeg", "image/jpg"]


def verify_file(mime_type: str) -> bool:
    """Returns true if the given filename is in the allowed list."""
    return mime_type in ALLOWED_EXTENSIONS


def file_extension(filename: str) -> str:
    return re.split(r"(?=\.)", filename)[-1]
