import resources.utils as utils
import uuid
from werkzeug.datastructures import FileStorage
from db.database import query, commit, rollback
from dataclasses import dataclass
import os
from typing import Tuple
from validation.forms import CreateObraForm

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
    work_id = query(
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
        rollback()
        raise e

    commit()
    return work_id


def delete_obra(id: int):
    obra = get_obra_by_id(id)

    if not obra:
        return

    for image in obra.images:
        delete_image(image.filename)

    query(
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
        query(
            """
            UPDATE obra SET nombre = %s WHERE id = %s
        """,
            (nombre, id),
            commit=False,
        )
    if description:
        query(
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
                query(
                    """
                UPDATE imagen SET texto_alt = %s WHERE archivo = %s
                """,
                    (alt_text, filename),
                    commit=False,
                )
            if (
                index is not None
            ):  # Not use 'if not index:' because if index = 0 then it should trigger but 0 == False
                query(
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

    commit()


def get_obra_by_id(id: int) -> Obra | None:
    """Returns the obra matching the given id or None."""
    data = query(
        """
    SELECT obra.id, nombre, descripcion, archivo, texto_alt, indice FROM obra LEFT JOIN imagen ON obra.id = imagen.obra_id 
    WHERE obra.id = %s;
    """,
        (id,),
    )

    if not data:
        return None

    obra = Obra(
        data[0][0],
        data[0][1],
        data[0][2],
        [Image(image[3], image[4], image[5]) for image in data],
    )

    return obra


def get_image(filename: str) -> Image | None:
    res = query(
        """
    SELECT archivo, texto_alt FROM imagen WHERE archivo = %s;
    """,
        (filename,),
        1,
    )

    image = None

    if res:
        image = Image(res[0], res[1])

    return image


def get_obras(page: int = 1, page_size: int = 10) -> list[Obra]:
    """Retrieves a list of obras. Paginated by the given size"""
    offset = (page - 1) * page_size

    data = query(
        """
        SELECT obra.id, nombre, descripcion, archivo, texto_alt, indice FROM obra LEFT JOIN imagen ON obra.id = imagen.obra_id 
        LIMIT %s OFFSET %s;
    """,
        (page_size, offset),
    )

    obras: list[Obra] = []

    for obra in data:
        id = obra[0]
        name = obra[1]
        description = obra[2]
        image = obra[3]
        alt_text = obra[4]
        index = obra[5]

        registered_obra = next((obra for obra in obras if obra.id == id), None)

        # If the current obra has been registered only save the images.
        if registered_obra:
            registered_obra.images.append(Image(image, alt_text, index))
        else:
            obra = Obra(id, name, description, [])
            obra.images.append(Image(image, alt_text))
            obras.append(obra)

    return obras


def get_obras_by_name(name: str, page: int = 1, page_size: int = 10):
    """Returns all the obras like a given name. Paginated."""
    # Code repetition bad and single source of truth stfu.
    offset = (page - 1) * page_size
    data = query(
        """
        SELECT obra.id, nombre, descripcion, archivo, texto_alt FROM obra LEFT JOIN imagen ON obra.id = imagen.obra_id
        WHERE obra.nombre ILIKE %s
        LIMIT %s OFFSET %s;
    """,
        (f"%{name}%", page_size, offset),
    )

    # Store it in a dict for faster id lookup. Then just return the values
    obras: dict[int, Obra] = {}

    for obra in data:
        id = obra[0]
        name = obra[1]
        description = obra[2]
        image = obra[3]
        alt_text = obra[4]

        registered_obra = obras.get(id)

        # If the current obra has been registered only save the images.
        if registered_obra:
            registered_obra.images.append(Image(image, alt_text))
        else:
            obra = Obra(id, name, description, [])
            obra.images.append(Image(image, alt_text))
            obras[id] = obra

    return list(obras.values())


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
        rollback()
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
        query(
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
        query(
            """
        DELETE FROM imagen WHERE archivo = %s
        """,
            (filename,),
        )

        os.remove(location)
