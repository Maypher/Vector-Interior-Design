from db import query
from dataclasses import dataclass

STORAGE_LOCATION = "/storage/images/"


@dataclass
class Image:
    filename: str
    alt_text: str
    index: int


@dataclass
class Obra:
    id: int
    name: str
    description: str
    images: list[Image]


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

    obras: dict[int, Obra] = {}

    for obra in data:
        id = obra[0]
        name = obra[1]
        description = obra[2]
        image = obra[3]
        alt_text = obra[4]
        index = obra[5]

        registered_obra = obras.get(id)

        # If the current obra has been registered only save the images.
        if registered_obra:
            registered_obra.images.append(Image(image, alt_text, index))
        else:
            obra = Obra(id, name, description, [])
            obra.images.append(Image(image, alt_text, index))
            obras[id] = obra

    return obras


def get_obras_by_name(name: str, page: int = 1, page_size: int = 10):
    """Returns all the obras like a given name. Paginated."""
    # Code repetition bad and single source of truth stfu.
    offset = (page - 1) * page_size
    data = query(
        """
        SELECT obra.id, nombre, descripcion, archivo, texto_alt, indice FROM obra LEFT JOIN imagen ON obra.id = imagen.obra_id
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
        index = obra[5]

        registered_obra = obras.get(id)

        # If the current obra has been registered only save the images.
        if registered_obra:
            registered_obra.images.append(Image(image, alt_text, index))
        else:
            obra = Obra(id, name, description, [])
            obra.images.append(Image(image, alt_text, index))
            obras[id] = obra

    return list(obras.values())
