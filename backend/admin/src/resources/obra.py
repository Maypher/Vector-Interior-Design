import resources.utils as utils
import uuid
from werkzeug.datastructures import FileStorage
from db.database import admin_database
from dataclasses import dataclass
import os
from typing import Tuple
from common.obra import *

STORAGE_LOCATION = "/storage/images/"


@dataclass
class Image:
    filename: str
    alt_text: str
    indices: int


@dataclass
class Obra:
    id: int
    name: str
    description: str
    images: list[Image]


def new_obra(
    name: str,
    description: str,
    images: list[FileStorage],
    alt_texts: list[
        dict[str, str]
    ],  # Here's in the format {filename: str, alt_text: str}
):
    """Creates a new obra. Data validation is assumed."""
    work_id = admin_database.query(
        """
    INSERT INTO obra (nombre, descripcion) VALUES (%s, %s) RETURNING id;
    """,
        (name, description),
        1,
        False,
    )[0]

    try:
        # Zip up images and alt text to get [(image, alt text)]
        new_images(
            [
                (image, alt_text["alt_text"])
                for image, alt_text in zip(images, alt_texts)
            ],
            work_id,
        )
    except Exception as e:
        admin_database.rollback()
        raise e

    admin_database.commit()
    return work_id


def delete_obra(id: int):
    obra = get_obra_by_id(id)

    if not obra:
        return

    for image in obra.images:
        delete_image(image.filename)

    admin_database.query(
        """
    DELETE FROM obra WHERE id = %s
    """,
        (id,),
    )


def update_obra(
    id: int,
    nombre: str | None = None,
    description: str | None = None,
    images_to_delete: list[Image] | None = None,
    images_change: list[str] | None = None,
    images_new: Tuple[(FileStorage, dict[str, str | int])] | None = None,
):
    """
    Updates the obra identified by id. Name and description can be updated, images can be removed or alt text changed.

    :param id: The id of the obra to change.
    :param nombre: The new name of the obra.
    :param description: The new description of the obra.
    :param images_to_delete: A list of images to delete. (filename)
    :param images_change: A list of images to change. ({filename: "file to change", alt_text: "new alt text", "index": "new index"})
    :param images_new: A list of new images. ((FileStorage, {filename: str, alt_text: str, index: int}), ...)
    """

    obra = get_obra_by_id(id)

    if not obra:
        return

    if nombre:
        admin_database.query(
            """
            UPDATE obra SET nombre = %s WHERE id = %s
        """,
            (nombre, id),
            commit=False,
        )
    if description:
        admin_database.query(
            """
            UPDATE obra SET descripcion = %s WHERE id = %s
        """,
            (description, id),
            commit=False,
        )
    if images_change:
        for image in images_change:
            alt_text = image.get("alt_text")
            index = image.get("index")
            filename = image["filename"]

            if alt_text:
                admin_database.query(
                    """
                UPDATE imagen SET texto_alt = %s WHERE archivo = %s
                """,
                    (alt_text, filename),
                    commit=False,
                )
            if (
                index is not None
            ):  # Not use 'if not index:' because if index = 0 then it should trigger but 0 == False
                admin_database.query(
                    """
                UPDATE imagen SET indice = %s WHERE archivo = %s
                """,
                    (index, filename),
                    commit=False,
                )
    if images_to_delete:
        for image in images_to_delete:
            delete_image(image.filename)
    if images_new:
        print([(image[0], image[1]["alt_text"]) for image in images_new], id)
        new_images([(image[0], image[1]["alt_text"]) for image in images_new], id)

    admin_database.commit()


def new_image(
    image: FileStorage,
    alt_text: str,
    work_id: int,
) -> str | None:
    """
    Saves an image to disk relating it to the given work and returns its unique filename.
    Returns None if image is unsupported or if given obra doesn't exist.
    """
    if not utils.verify_file(image.filename):
        admin_database.rollback()
        return

    obra = get_obra_by_id(work_id)

    if not obra:
        return

    file_extension = utils.file_extension(image.filename)

    image_name = uuid.uuid4().hex
    image.filename = image_name + file_extension
    image_location = f"{STORAGE_LOCATION}{image.filename}"

    image.save(image_location)

    # If for any reason the image doesn't save to the database remove it from storage and propagate the error.
    try:
        admin_database.query(
            """
        INSERT INTO imagen (archivo, texto_alt, obra_id) VALUES (%s, %s, %s);
        """,
            (image.filename, alt_text, work_id),
        )
    except Exception as e:
        os.remove(image_location)
        raise e

    return image.filename


def new_images(images: list[Tuple[FileStorage, str]], work_id):
    """
    Used to save multiple images at once. If one image fails to save all images are rolled back.

    :param images: The images to create. (FileStorage, alt_text)
    """
    saved_images = []

    for image, alt_text in images:
        try:
            filename = new_image(image, alt_text, work_id)
            if not filename:
                raise ValueError(f"Ninguna obra con el ID {work_id} existe.")
        except Exception as e:
            for image in saved_images:
                delete_image(filename)
            raise e


def delete_image(filename: str):
    """Deletes the given image from the database and file system."""
    location = f"{STORAGE_LOCATION}{filename}"
    if os.path.exists(location):
        admin_database.query(
            """
        DELETE FROM imagen WHERE archivo = %s
        """,
            (filename,),
        )

        os.remove(location)
