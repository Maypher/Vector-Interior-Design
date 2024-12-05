import resources.utils as utils
import uuid
from werkzeug.datastructures import FileStorage
from db.database import admin_database
import os
from common.obra import *

STORAGE_LOCATION = "/storage/images/"


def create_obra(name: str, description: str):
    """Creates a new obra. Data validation is assumed."""
    work_id = admin_database.query(
        """
    INSERT INTO obra (nombre, descripcion) VALUES (%s, %s) RETURNING id;
    """,
        (name, description),
        1,
    )[0]

    return work_id


def delete_obra(id: int):
    """
    Deletes the obra identified by id alongside its related ambientes and images.
    """
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
    public: bool | None = None,
):
    """
    Updates the obra identified by id. Name and description can be updated.

    :param id: The id of the obra to change.
    :param nombre: The new name of the obra.
    :param description: The new description of the obra.
    """

    obra = get_obra_by_id(id, True)

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

    if public is not None:
        admin_database.query(
            """
            UPDATE obra SET publico = %s WHERE id = %s
        """,
            (public, id),
            commit=False,
        )

    admin_database.commit()


def create_ambiente(obra_id: int, name: str, description: str | None = None) -> int:
    """Creates a new ambiente for the given obra"""

    ambiente_id = admin_database.query(
        """
    INSERT INTO ambiente (nombre, descripcion, obra_id) VALUES (%s, %s, %s) RETURNING id;
    """,
        (name, description, obra_id),
        1,
    )[0]

    return ambiente_id


def update_ambiente(
    id: int,
    new_name: str | None = None,
    new_description: str | None = None,
    new_index: int | None = None,
):
    """
    Updates the ambiente identified by id. Name and description can be updated.

    :param id: The id of the ambiente to change.
    :param new_name: The new name of the ambiente.
    :param description: The new description of the ambiente.
    :param index: The new index of the ambiente inside obra.
    """
    ambiente = get_ambiente_by_id(id)

    print(ambiente)

    if not ambiente:
        return

    if new_name:
        admin_database.query(
            """
            UPDATE ambiente SET nombre = %s WHERE id = %s
        """,
            (new_name, id),
            commit=False,
        )
    if new_description:
        admin_database.query(
            """
            UPDATE ambiente SET descripcion = %s WHERE id = %s
        """,
            (new_description, id),
            commit=False,
        )
    if new_index is not None:
        # Done this way because if new_index = 0 then the condition fails
        admin_database.query(
            """
            UPDATE ambiente SET indice = %s WHERE id = %s
        """,
            (new_index, id),
            commit=False,
        )

    admin_database.commit()


def delete_ambiente(id: int):
    """
    Deletes the ambiente identified by id alongside all images related to it.
    """
    ambiente = get_ambiente_by_id(id)

    if not ambiente:
        return

    # Image are collated in database but they also need to be removed from the filesystem
    for image in ambiente.images:
        delete_image(image.filename)

    admin_database.query(
        """
    DELETE FROM ambiente WHERE id = %s
    """,
        (id,),
    )


def create_image(
    image: FileStorage,
    alt_text: str,
    ambiente_id: int,
) -> str | None:
    """
    Saves an image to disk relating it to the given work and returns its unique filename.
    Returns None if image is unsupported or if given obra doesn't exist.
    """
    if not utils.verify_file(image.filename):
        admin_database.rollback()
        return

    ambiente = get_ambiente_by_id(ambiente_id)

    if not ambiente:
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
        INSERT INTO imagen (archivo, texto_alt, ambiente_id) VALUES (%s, %s, %s);
        """,
            (image.filename, alt_text, ambiente.id),
        )
    except Exception as e:
        os.remove(image_location)
        raise e

    return image.filename


def update_image(filename: int, alt_text: str | None = None, index: int | None = None):
    """
    Updates the alt text of the given image.
    """

    if alt_text:
        admin_database.query(
            """
            UPDATE imagen SET texto_alt = %s WHERE archivo = %s
            """,
            (alt_text, filename),
        )
    if index is not None:
        print("new index", index)
        # Done this way because if index = 0 then the condition fails
        admin_database.query(
            """
            UPDATE imagen SET indice = %s WHERE archivo = %s
            """,
            (index, filename),
        )


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
