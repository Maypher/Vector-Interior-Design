import re

ALLOWED_EXTENSIONS = ["png", "jpeg", "jpg"]


def verify_file(filename: str) -> bool:
    """Returns true if the given filename is in the allowed list."""
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


def file_extension(filename: str) -> str:
    return re.split(r"(?=\.)", filename)[-1]
