import resources.utils as utils
import uuid
from werkzeug.datastructures import FileStorage
from db.database import query, commit, rollback
from dataclasses import dataclass
import os

STORAGE_LOCATION = "/storage/images/"


@dataclass
class Image:
    filename: str
    alt_text: str


@dataclass
class Obra:
    id: int
    name: str
    description: str
    images: list[Image]


def new_obra(
    name: str, description: str, images: list[FileStorage], alt_texts: list[str]
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

    # Zip up images and alt text to get [(image, alt text)]
    for image, alt_text in zip(images, alt_texts):
        try:
            new_image(image, alt_text, work_id)
        except Exception as e:
            rollback()
            return f"Unable to save {image.filename} due to an error. {e}", 500

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
    alt_text_change: list[Image] | None = None,
    images_to_add: list[(FileStorage, str)] | None = None,
):
    """Updates the obra identified by id. Name and description can be updated, images can be removed or alt text changed."""

    obra = get_obra_by_id(id)

    if not obra:
        return

    if nombre:
        query(
            """
            UPDATE obra SET name = %s WHERE id = %s
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
    if alt_text_change:
        for image in alt_text_change:
            query(
                """
            UPDATE imagen SET texto_alt = %s WHERE archivo = %s
            """,
                (image.alt_text, image.filename),
                commit=False,
            )
    if images_to_delete:
        for image in images_to_delete:
            delete_image(image.filename)
    if images_to_add:
        for image, alt_text in images_to_add:
            new_image(image, alt_text, id)

    commit()


def get_obra_by_id(id: int) -> Obra | None:
    """Returns the obra matching the given id or None."""
    data = query(
        """
    SELECT obra.id, nombre, descripcion, archivo, texto_alt FROM obra LEFT JOIN imagen ON obra.id = imagen.obra_id 
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
        [Image(image[3], image[4]) for image in data],
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
        SELECT obra.id, nombre, descripcion, archivo, texto_alt FROM obra LEFT JOIN imagen ON obra.id = imagen.obra_id 
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

        registered_obra = next((obra for obra in obras if obra.id == id), None)

        # If the current obra has been registered only save the images.
        if registered_obra:
            registered_obra.images.append(Image(image, alt_text))
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


def new_image(image: FileStorage, alt_text: str, work_id: int) -> str | None:
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

    # If for any reason the image doesn't data doesn't save to the database remove it from storage and propagate the error.
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


def delete_image(filename: str):
    """Deletes the given image from the database and file system."""
    location = f"{STORAGE_LOCATION}{filename}"
    if os.path.exists(location):
        query(
            """
        DELETE FROM imagen WHERE archivo = %s
        """,
            (filename,),
            commit=False,
        )

        os.remove(location)

        commit()
