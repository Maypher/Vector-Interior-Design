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
        if not utils.verify_file(image.filename):
            rollback()
            return f"file {image.filename} is of an unsupported type", 400

        file_extension = utils.file_extension(image.filename)

        image_name = uuid.uuid4().hex
        image.filename = image_name + file_extension

        image.save(f"{STORAGE_LOCATION}{image.filename}")

        print("Work id", work_id)

        query(
            """
        INSERT INTO imagen (archivo, texto_alt, obra_id) VALUES (%s, %s, %s);
        """,
            (image.filename, alt_text, work_id),
            commit=False,
        )

    commit()
    return work_id


def delete_obra(id: int):
    obra = get_obra_by_id(id)

    if not obra:
        return

    for image in obra.images:
        delete_image_from_storage(image.filename)

    query(
        """
    DELETE FROM obra WHERE id = %s
    """,
        (id,),
    )


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


def delete_image_from_storage(filename: str):
    location = f"{STORAGE_LOCATION}{filename}"
    if os.path.exists(location):
        os.remove(location)
