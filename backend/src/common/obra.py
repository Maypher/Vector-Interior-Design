from dataclasses import dataclass
from common.database import generic_database
from math import ceil


@dataclass
class Image:
    filename: str
    alt_text: str
    index: int


@dataclass
class Ambiente:
    id: int
    name: str
    description: str | None
    index: int
    images: list[Image]


@dataclass
class Obra:
    id: int
    name: str
    description: str
    area: int
    imagen_principal: str | None
    ambientes: list[Ambiente]
    public: bool


def get_obra_by_id(id: int, allow_private: bool = False) -> Obra | None:
    """Returns the obra matching the given id or None."""
    data = generic_database.query(
        f"""
    SELECT obra.id, nombre, descripcion, imagen_principal, publico, area FROM obra
    WHERE obra.id = %s {"AND publico" if not allow_private else ""};
    """,
        (id,),
        1,
    )

    if not data:
        return None

    obra_id = int(data[0])
    name = data[1]
    description = data[2]
    thumbnail_id = data[3]
    publico = data[4]
    area = data[5]

    thumbnail = generic_database.query(
        """
        SELECT archivo FROM imagen WHERE id = %s;
        """,
        (thumbnail_id,),
        1,
    )

    obra = Obra(
        obra_id,
        name,
        description,
        area,
        thumbnail[0] if thumbnail else None,
        get_ambientes_by_obra(obra_id),
        publico,
    )

    return obra


def get_obras(
    page: int = 1, page_size: int = 10, allow_private: bool = False
) -> list[Obra]:
    """Retrieves a list of obras. Paginated by the given size"""
    offset = (page - 1) * page_size

    obra_ids = generic_database.query(
        f"""
        SELECT id FROM obra {"WHERE publico" if not allow_private else ""} 
        LIMIT %s OFFSET %s;
    """,
        (page_size, offset),
    )

    # I know this isn't the most efficient way but there will be at most 30 obras so ＜（＾－＾）＞.
    obras_count = generic_database.query(
        f"""
    SELECT COUNT(*) FROM obra {"WHERE publico" if not allow_private else ""};
    """,
        count=1,
    )[0]

    page_count = ceil(obras_count / page_size)

    return {
        "page": page,
        "page_count": page_count,
        "obras": [
            obra
            for id in obra_ids
            if (obra := get_obra_by_id(id[0], allow_private)) is not None
        ],
    }


def get_obras_by_name(
    name: str, page: int = 1, page_size: int = 10, allow_private: bool = False
):
    """Returns all the obras like a given name. Paginated."""
    # Code repetition bad and single source of truth stfu.
    offset = (page - 1) * page_size
    obra_ids = generic_database.query(
        f"""
        SELECT id FROM obra
        WHERE obra.nombre ILIKE %s {"AND publico" if not allow_private else ""}
        LIMIT %s OFFSET %s;
    """,
        (f"%{name}%", page_size, offset),
    )

    obras_count = generic_database.query(
        f"""
    SELECT COUNT(*) FROM obra WHERE obra.nombre ILIKE %s {"AND publico" if not allow_private else ""};
    """,
        (f"%{name}%",),
        1,
    )[0]

    page_count = ceil(obras_count / page_size)

    return {
        "page": page,
        "page_count": page_count,
        "obras": [
            obra
            for id in obra_ids
            if (obra := get_obra_by_id(id[0], allow_private)) is not None
        ],
    }


def get_ambiente_by_id(id: int) -> Ambiente | None:
    """Returns the ambiente matching the given id or None."""

    data = generic_database.query(
        """
    SELECT ambiente.id, nombre, descripcion, ambiente.indice, archivo, texto_alt, imagen.indice 
    FROM ambiente LEFT JOIN imagen ON ambiente.id = imagen.ambiente_id 
    WHERE ambiente.id = %s;
    """,
        (id,),
    )

    if not data:
        return None

    ambiente_id = data[0][0]
    nombre = data[0][1]
    description = data[0][2]
    index = data[0][3]
    images = []

    for entry in data:
        image_data = entry[4:]
        filename = image_data[0]
        alt_text = image_data[1]
        img_index = image_data[2]

        if filename and alt_text and img_index is not None:
            images.append(Image(filename, alt_text, img_index))

    ambiente = Ambiente(ambiente_id, nombre, description, index, images)

    return ambiente


def get_ambientes_by_obra(obra_id: int) -> list[Ambiente]:
    """Returns all ambientes for the given obra_id."""

    found_ambientes = generic_database.query(
        """
    SELECT ambiente.id 
    FROM obra INNER JOIN ambiente ON ambiente.obra_id = obra.id 
    WHERE obra.id = %s;
    """,
        (obra_id,),
    )

    return [get_ambiente_by_id(int(id[0])) for id in found_ambientes]
