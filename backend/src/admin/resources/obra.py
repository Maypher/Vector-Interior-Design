import resources.utils as utils
import uuid
from werkzeug.datastructures import FileStorage
from db.database import admin_database
import os
from common.obra import *
from psycopg import errors
from psycopg.sql import SQL, Identifier
from math import ceil, floor
from common.common_graphql import schemas
from admin.resources.admin_graphql import errors as GraphqlErrors

STORAGE_LOCATION = "/storage/images/"


def create_obra(name: str, description: str, area: int) -> schemas.Obra:
    """Creates a new obra. Data validation is assumed."""
    obra_data = admin_database.query(
        """
    INSERT INTO obra (nombre, descripcion, area) VALUES (%s, %s, %s) RETURNING id, nombre, descripcion, area, indice, publico;
    """,
        (name, description, area),
        1,
    )

    return schemas.Obra(
        id=obra_data[0],
        name=obra_data[1],
        description=obra_data[2],
        area=obra_data[3],
        index=obra_data[4],
        public=obra_data[5],
    )


def delete_obra(id: int) -> typing.Optional[schemas.Obra]:
    """
    Deletes the obra identified by id alongside its related ambientes and images.
    """
    obra = get_obra_by_id(id, allow_private=True)

    print(obra)

    if not obra:
        return

    for ambiente in obra.ambientes():
        for image in ambiente.images():
            delete_image(image.filename)

    admin_database.query(
        """
    DELETE FROM obra WHERE id = %s RETURNING id;
    """,
        (id,),
        count=1,
    )[0]

    return obra


def update_obra(
    id: int,
    name: str | None = None,
    description: str | None = None,
    area: int | None = None,
    thumbnail: str | None = None,
    index: int | None = None,
    public: bool | None = None,
) -> typing.Optional[schemas.Image]:
    """
    Updates the obra identified by id returning the updated obra or None if no obra was found.

    :param id: The id of the obra to change.
    :param name: The new name of the obra.
    :param area: The area of the obra in meters squared.
    :param thumbnail: The image that should be the thumbnail of this obra. Set to False to remove it.
    :param index: The new index of the obra. Used to show the obras in order in the UI.
    :param description: The new description of the obra.
    """

    obra = get_obra_by_id(id, True)

    if not obra:
        return

    if name:
        admin_database.query(
            """
            UPDATE obra SET nombre = %s WHERE id = %s
        """,
            (name, id),
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
    if area:
        admin_database.query(
            """
            UPDATE obra SET area = %s WHERE id = %s
        """,
            (area, id),
            commit=False,
        )
    if thumbnail:
        image = admin_database.query(
            """
            SELECT id FROM imagen WHERE archivo = %s;
            """,
            (thumbnail,),
            1,
        )[0]

        if image:
            admin_database.query(
                """
                UPDATE obra SET imagen_principal = %s WHERE id = %s;
                """,
                (image, obra.id),
            )
    elif not thumbnail:
        admin_database.query(
            """
                UPDATE obra SET imagen_principal = NULL WHERE id = %s;
                """,
            (obra.id,),
        )
    if index is not None:
        update_index(id, "obra", index)
    if public is not None:
        admin_database.query(
            """
            UPDATE obra SET publico = %s WHERE id = %s
        """,
            (public, id),
            commit=False,
        )

    admin_database.commit()
    return get_obra_by_id(id, True)


def create_ambiente(
    obra_id: int, name: str, description: typing.Optional[str]
) -> typing.Optional[schemas.Ambiente]:
    """Creates a new ambiente for the given obra"""

    obra = get_obra_by_id(obra_id, True)

    if not obra:
        return GraphqlErrors.ObraNotFoundAmbiente(obra_id=obra_id)

    ambiente = admin_database.query(
        """
    INSERT INTO ambiente (nombre, descripcion, obra_id) VALUES (%s, %s, %s) RETURNING id, nombre, descripcion, indice;
    """,
        (name, description, obra_id),
        1,
    )

    return schemas.Ambiente(
        id=ambiente[0], name=ambiente[1], description=ambiente[2], index=ambiente[3]
    )


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
    :param index: The new zero-based index of the ambiente inside obra.
    """
    ambiente = get_ambiente_by_id(id, True)

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
    if (
        new_description or new_description == ""
    ):  # Done this way because if the new description is blank it should be removed
        admin_database.query(
            """
            UPDATE ambiente SET descripcion = %s WHERE id = %s
        """,
            (new_description, id),
            commit=False,
        )
    if new_index is not None:
        obra_id = admin_database.query(
            """
        SELECT obra_id FROM ambiente WHERE id = %s
        """,
            (ambiente.id,),
            count=1,
        )[0]

        update_index(id, "ambiente", new_index, "obra_id", obra_id)

    admin_database.commit()
    return get_ambiente_by_id(id, True)


def delete_ambiente(id: int) -> typing.Optional[schemas.Ambiente]:
    """
    Deletes the ambiente identified by id alongside all images related to it.
    """
    ambiente = get_ambiente_by_id(id, True)

    if not ambiente:
        return

    # Image are collated in database but they also need to be removed from the filesystem
    for image in ambiente.images():
        delete_image(image.filename)

    admin_database.query(
        """
    DELETE FROM ambiente WHERE id = %s
    """,
        (id,),
    )

    return ambiente


def create_image(
    image: FileStorage,
    alt_text: str,
    ambiente_id: int,
) -> typing.Union[
    schemas.Image,
    GraphqlErrors.UnsupportedFileType,
    GraphqlErrors.AmbienteNotFoundImage,
]:
    """
    Saves an image to disk relating it to the given work and returns its unique filename.
    Returns None if image is unsupported or if given obra doesn't exist.
    """
    if not utils.verify_file(image.filename):
        admin_database.rollback()
        return GraphqlErrors.UnsupportedFileType(filetype=image.mimetype)

    ambiente = get_ambiente_by_id(ambiente_id, True)

    if not ambiente:
        return GraphqlErrors.AmbienteNotFoundImage(ambiente_id=ambiente_id)

    file_extension = utils.file_extension(image.filename)

    image_name = uuid.uuid4().hex
    image.filename = image_name + file_extension
    image_location = f"{STORAGE_LOCATION}{image.filename}"

    image.save(image_location)

    # If for any reason the image doesn't save to the database remove it from storage and propagate the error.
    try:
        data = admin_database.query(
            """
        INSERT INTO imagen (archivo, texto_alt, ambiente_id) VALUES (%s, %s, %s)
        RETURNING id, archivo, texto_alt, indice;
        """,
            (image.filename, alt_text, ambiente.id),
            count=1,
        )
    except Exception as e:
        os.remove(image_location)
        raise e

    return schemas.Image(id=data[0], filename=data[1], alt_text=data[2], index=data[3])


def update_image(
    filename: str, alt_text: str | None = None, new_index: int | None = None
) -> typing.Optional[schemas.Image]:
    """
    Updates the alt text of the given image.

    :param filename: The filename of the image to update.
    :param alt_text: The new alt text of the image.
    :param new_index: The zero-based index where to move the image to.
    """

    image = admin_database.query(
        """SELECT id, ambiente_id FROM imagen WHERE archivo = %s""", (filename,), 1
    )

    if not image:
        return

    if alt_text:
        admin_database.query(
            """
            UPDATE imagen SET texto_alt = %s WHERE id = %s
            """,
            (alt_text, image[0]),
            commit=False,
        )
    if new_index is not None:
        update_index(image[0], "imagen", new_index, "ambiente_id", image[1])

    admin_database.commit()
    return get_image_by_filename(filename)


def delete_image(filename: str) -> typing.Optional[schemas.Image]:
    """Deletes the given image from the database and file system."""

    image = get_image_by_filename(filename)

    if not image:
        return

    location = f"{STORAGE_LOCATION}{filename}"
    if os.path.exists(location):
        admin_database.query(
            """
        DELETE FROM imagen WHERE archivo = %s
        """,
            (filename,),
        )

        os.remove(location)
        return image


def update_index(
    element_id: int,
    tablename: str,
    new_index: int,
    where_col: str | None = None,
    parent_id: int | None = None,
):
    """
    Updates the index of given element in the given table.
    The new index is passed as an integer but is transformed into a float to avoid having to update every entry in the database.
    Doesn't commit.

    :param element_id: The `id` of the element to update the index of.
    :param tablename: The table in which the element is stored.
    :param new_index: The zero-based index of where to put the element. It should be a zero-based integer.
    :param where_col: For ambientes and imagenes. Used to filter by obra/ambiente.
    :param parent_id: The id of the element to filter `where_col` by.
    For example, to put an element in the second position it should be index 1.
    """

    max_index = admin_database.query(
        SQL(
            f"SELECT COUNT(*) FROM {{}} {SQL("WHERE {} = {}".format(Identifier(where_col), parent_id)) if where_col else ''};"
        ).format(Identifier(tablename)),
        count=1,
    )[0]

    # Clamp the new index between 0 and max index
    offset = min(max(new_index, 0), int(max_index) - 1)

    # Get the indices of the elements before and after the new insertion.
    indices_around = admin_database.query(
        SQL(
            f"SELECT id, indice FROM {{}} ORDER BY indice OFFSET {{}} LIMIT {2 if offset > 0 else 1};"  # Done this way because if the offset is 0 then that means it's being moved to the begging so only fetch the first element
        ).format(Identifier(tablename), offset, element_id)
    )

    # If there's only one indice it means its being moved to the end or beginning.
    if len(indices_around) == 1:
        if offset > 0:
            # If the offset is greater than zero it means the element is moved to end.
            admin_database.query(
                SQL("UPDATE {} SET indice = nextval({}) WHERE id = {}").format(
                    Identifier(tablename), f"{tablename}_indice_seq", element_id
                )
            )
        else:
            # If the offset is zero it means that the element is being moved to the beginning

            final_index = indices_around[0][1] / 2

            try:
                admin_database.query(
                    SQL("UPDATE {} SET indice = {} WHERE id = {};").format(
                        Identifier(tablename), final_index, element_id
                    ),
                )
            except errors.UniqueViolation:
                # This means that the precision limit has been reached and should be refactored
                fix_precision_limit(tablename, final_index)
                # Insert the element again since it failed last time
                update_index(element_id, tablename, new_index)
    elif indices_around[0][0] == element_id:
        # If the element itself is selected it means the two values are being swapped around.

        sel_id = indices_around[1][0]

        admin_database.query(
            SQL(
                """
                UPDATE {0}
                SET indice = CASE
                    WHEN id = {1} THEN (SELECT indice FROM {0} WHERE id = {2})
                    WHEN id = {2} THEN (SELECT indice FROM {0} WHERE id = {1})
                END
                WHERE id IN ({1}, {2});
            """
            ).format(Identifier(tablename), element_id, sel_id)
        )
    elif indices_around[1][0] == element_id:
        # If the element itself is the element after it means it's being updated to its same position so just ignore it.
        return
    else:
        # Move the element to the desired position

        before_index = indices_around[0][1]
        after_index = indices_around[1][1]
        final_index = (before_index + after_index) / 2

        try:
            admin_database.query(
                SQL("UPDATE {} SET indice = {} WHERE id = {};").format(
                    Identifier(tablename), final_index, element_id
                ),
            )
        except errors.UniqueViolation:
            # This means that the precision limit has been reached and should be refactored
            fix_precision_limit(tablename, final_index)
            # Insert the element again since it failed last time
            update_index(element_id, tablename, new_index)


def fix_precision_limit(tablename: str, index_range: int):
    """
    Reorganizes the indexes of the given tablename around the `index_range`.
    This is used when reordering has reached its precision limit.
    """

    upper_bound = ceil(index_range)
    lower_bound = floor(index_range)

    entries_to_update = admin_database.query(
        SQL(
            "SELECT id, indice FROM {} WHERE indice > {} AND indice < {} SORT BY indice;"
        ).format(Identifier(tablename), lower_bound, upper_bound),
    )

    # How much space to leave between elements to spread them evenly
    interval_between_indices = 1 / len(entries_to_update)

    for index, id in enumerate(entries_to_update, 1):
        admin_database.query(
            SQL(
                """
            UPDATE {} SET indice = {} = {} WHERE id = {};
            """
            ).format(
                Identifier(tablename),
                lower_bound + interval_between_indices * index,
                id,
            ),
        )
