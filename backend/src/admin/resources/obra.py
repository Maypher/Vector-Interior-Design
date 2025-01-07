from admin import utilities
import uuid
import os
from common.obra import *
from psycopg import errors
from psycopg.sql import SQL, Identifier
from math import ceil, floor
from common.common_graphql import schemas
from admin.resources.admin_graphql import errors as GraphqlErrors
from admin.resources.admin_graphql import inputs
from admin.db.database import AdminDatabaseManager
from common.obra import ResourceManager
from strawberry import UNSET
from sanic.request.form import File
import aiofiles

STORAGE_LOCATION = "/storage/images/"


class AdminResourceManager(ResourceManager):
    def __init__(self, database_manager: AdminDatabaseManager):
        self.database_manager = database_manager
        self.allow_private = True

    def create_obra(self, name: str, description: str, area: int) -> schemas.Obra:
        """Creates a new obra. Data validation is assumed."""
        obra_data = self.database_manager.query(
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

    def delete_obra(self, id: int) -> bool:
        """
        Deletes the obra identified by id alongside its related ambientes and images.
        """
        obra = self.get_obra_by_id(id)

        if not obra:
            return False

        for ambiente in obra.ambientes():
            for image in ambiente.images():
                self.datdelete_image(image.filename)

        self.database_manager.query(
            """
        DELETE FROM obra WHERE id = %s RETURNING id;
        """,
            (id,),
            count=1,
        )[0]

        return True

    def update_obra(
        self,
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

        obra = self.get_obra_by_id(id)

        if not obra:
            return

        if name:
            self.database_manager.query(
                """
                UPDATE obra SET nombre = %s WHERE id = %s
            """,
                (name, id),
                commit=False,
            )
        if description:
            self.database_manager.query(
                """
                UPDATE obra SET descripcion = %s WHERE id = %s
            """,
                (description, id),
                commit=False,
            )
        if area:
            self.database_manager.query(
                """
                UPDATE obra SET area = %s WHERE id = %s
            """,
                (area, id),
                commit=False,
            )
        if thumbnail is not UNSET:
            if thumbnail is None:
                image = None
            else:
                image = self.database_manager.query(
                    """
                    SELECT id FROM imagen WHERE archivo = %s;
                    """,
                    (thumbnail,),
                    1,
                )

                image = image[0] if image else None

            self.database_manager.query(
                """
                UPDATE obra SET imagen_principal = %s WHERE id = %s;
                """,
                (image, obra.id),
            )
        if index is not None:
            self.update_index(id, "obra", index)
        if public is not None:
            self.database_manager.query(
                """
                UPDATE obra SET publico = %s WHERE id = %s
            """,
                (public, id),
                commit=False,
            )

        self.database_manager.commit()
        return self.get_obra_by_id(id)

    def create_ambiente(
        self, obra_id: int, name: str, description: typing.Optional[str]
    ) -> typing.Optional[schemas.Ambiente]:
        """Creates a new ambiente for the given obra"""

        obra = self.get_obra_by_id(obra_id)

        if not obra:
            return GraphqlErrors.ObraNotFoundAmbiente(obra_id=obra_id)

        ambiente = self.database_manager.query(
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
        self,
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
        ambiente = self.get_ambiente_by_id(id)

        if not ambiente:
            return

        if new_name:
            self.database_manager.query(
                """
                UPDATE ambiente SET nombre = %s WHERE id = %s
            """,
                (new_name, id),
                commit=False,
            )
        if (
            new_description or new_description == ""
        ):  # Done this way because if the new description is blank it should be removed
            self.database_manager.query(
                """
                UPDATE ambiente SET descripcion = %s WHERE id = %s
            """,
                (new_description, id),
                commit=False,
            )
        if new_index is not None:
            obra_id = self.database_manager.query(
                """
            SELECT obra_id FROM ambiente WHERE id = %s
            """,
                (ambiente.id,),
                count=1,
            )[0]

            self.update_index(id, "ambiente", new_index, "obra_id", obra_id)

        self.database_manager.commit()
        return self.get_ambiente_by_id(id)

    def delete_ambiente(self, id: int) -> bool:
        """
        Deletes the ambiente identified by id alongside all images related to it.
        """
        ambiente = self.get_ambiente_by_id(id)

        if not ambiente:
            return False

        # Image are collated in database but they also need to be removed from the filesystem
        for image in ambiente.images():
            self.delete_image(image.filename)

        self.database_manager.query(
            """
        DELETE FROM ambiente WHERE id = %s
        """,
            (id,),
        )

        return True

    async def create_image(
        self,
        image: File,
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
        if not utilities.verify_file(image.type):
            self.database_manager.rollback()
            return GraphqlErrors.UnsupportedFileType(filetype=image.type)

        ambiente = self.get_ambiente_by_id(ambiente_id)

        if not ambiente:
            return GraphqlErrors.AmbienteNotFoundImage(ambiente_id=ambiente_id)

        file_extension = utilities.file_extension(image.name)

        image_name = uuid.uuid4().hex
        image_location = f"{STORAGE_LOCATION}{image_name}.{file_extension}"

        async with aiofiles.open(image_location, "w") as file:
            file.write(image.body)

        # If for any reason the image doesn't save to the database remove it from storage and propagate the error.
        try:
            data = self.database_manager.query(
                """
            INSERT INTO imagen (archivo, texto_alt, ambiente_id) VALUES (%s, %s, %s)
            RETURNING id, archivo, texto_alt, indice, pagina_principal, descripcion, descripcionTipografia, esconderEnObra;
            """,
                (image.name, alt_text, ambiente.id),
                count=1,
            )
        except Exception as e:
            os.remove(image_location)
            raise e

        return schemas.Image(
            id=data[0],
            filename=data[1],
            alt_text=data[2],
            index=data[3],
            main_page=data[4],
            description=data[5],
            description_font=data[6],
            hide_in_project=data[7],
        )

    def update_image(
        self,
        filename: str,
        alt_text: str | None = None,
        new_index: int | None = None,
        main_page: bool | None = None,
        hide_in_project: bool | None = None,
        description: str | None = None,
        descriptionFont: str | None = None,
        phone_config: inputs.phoneConfigInput | None = None,
    ) -> typing.Optional[schemas.Image]:
        """
        Updates the alt text of the given image.

        :param filename: The filename of the image to update.
        :param alt_text: The new alt text of the image.
        :param new_index: The zero-based index where to move the image to.
        """

        image = self.database_manager.query(
            """SELECT id, ambiente_id FROM imagen WHERE archivo = %s""", (filename,), 1
        )

        if not image:
            return

        image_id = image[0]

        if alt_text:
            self.database_manager.query(
                """
                UPDATE imagen SET texto_alt = %s WHERE id = %s
                """,
                (alt_text, image_id),
                commit=False,
            )
        if new_index is not None:
            self.update_index(image[0], "imagen", new_index, "ambiente_id", image[1])
        if main_page is not None:
            self.database_manager.query(
                """
                UPDATE imagen SET pagina_principal = %s WHERE id = %s;
                """,
                (main_page, image_id),
                commit=False,
            )

            if main_page:
                # Checks if the image already has config and if so it doesn't create a new one.
                self.database_manager.query(
                    """
                    INSERT INTO imagenConfig (imagen_id) SELECT %s
                    WHERE NOT EXISTS 
                    (SELECT 1 FROM imagenConfig JOIN imagen ON imagenConfig.imagen_id = imagen.id WHERE imagen.id = %s);
                """,
                    (image_id, image_id),
                )
        if hide_in_project is not None:
            self.database_manager.query(
                """
                UPDATE imagen SET esconderEnObra = %s WHERE id = %s;
                """,
                (hide_in_project, image_id),
                commit=False,
            )
        if description is not None:
            self.database_manager.query(
                """
                UPDATE imagen SET descripcion = %s WHERE id = %s;
                """,
                (description, image_id),
                commit=False,
            )
        if descriptionFont is not None:
            self.database_manager.query(
                """
                UPDATE imagen SET descripcionTipografia = %s WHERE id = %s;
                """,
                (descriptionFont, image_id),
                commit=False,
            )
        if phone_config:
            bit_string = "".join(
                "1" if b else "0" for b in (vars(phone_config.borders).values())
            )

            # Transform it into binary and then a string because if only binary
            # postgres treats it as a smallint and it fails
            borders = bin(int(bit_string, 2))
            borders = f"{bit_string}"

            self.database_manager.query(
                """
                UPDATE imagen SET tlfnConfig = ROW(%s, %s, %s, %s)::imagenTlfnConfig WHERE archivo = %s;
            """,
                (
                    borders,
                    phone_config.alignment,
                    phone_config.descriptionPos,
                    phone_config.descriptionAlignment,
                    filename,
                ),
                commit=False,
            )

        self.database_manager.commit()
        return self.get_image_by_filename(filename)

    def delete_image(self, filename: str) -> bool:
        """Deletes the given image from the database and file system."""

        image = self.get_image_by_filename(filename)

        if not image:
            return False

        location = f"{STORAGE_LOCATION}{filename}"
        if os.path.exists(location):
            self.database_manager.query(
                """
            DELETE FROM imagen WHERE archivo = %s;
            """,
                (filename,),
            )

            os.remove(location)
            return True
        return False

    def update_index(
        self,
        element_id: int,
        tablename: str,
        new_index: int,
        where_col: str | None = None,
        parent_id: int | None = None,
    ):
        """
        Updates the index of given element in the given table.
        The new index is passed as an integer but is transformed into a float to avoid having to update every entry in the database.
        Doesn't commit. For example, to put an element in the second position it should be index 1.

        :param element_id: The `id` of the element to update the index of.
        :param tablename: The table in which the element is stored.
        :param new_index: The zero-based index of where to put the element. It should be a zero-based integer.
        :param where_col: For ambientes and imagenes. Used to filter by obra/ambiente.
        :param parent_id: The id of the element to filter `where_col` by.
        """

        max_index = self.database_manager.query(
            SQL(
                f"SELECT COUNT(*) FROM {{}} {SQL("WHERE {} = {}".format(Identifier(where_col), parent_id)) if where_col else ''};"
            ).format(Identifier(tablename)),
            count=1,
        )[0]

        # Clamp the new index between 0 and max index
        # -1 because postgres offsets exclude the given value so offset 3 would remove 3 values and give the 4th
        new_index = min(max(new_index, 0), int(max_index) - 1)

        # region get indices of elements around the selected one

        # The index of the element before being updated
        current_index = self.database_manager.query(
            SQL(
                f"""
            SELECT indice FROM {{}} WHERE {f' "{where_col}" = {parent_id} and' if where_col else ''} id = {{}};
        """
            ).format(Identifier(tablename), element_id),
            count=1,
        )[0]

        # Transform the index from zero based to the database float version
        desired_pos_data = self.database_manager.query(
            SQL(
                f"""
            SELECT id, indice FROM {{}} {f'WHERE "{where_col}" = {parent_id}' if where_col else ''} ORDER BY indice OFFSET {{}} LIMIT 1; 
            """,
            ).format(Identifier(tablename), new_index),
            count=1,
        )

        desired_element_id = desired_pos_data[0] if desired_pos_data else None
        desired_index = desired_pos_data[1] if desired_pos_data else None

        if current_index > desired_index:
            index_before = self.database_manager.query(
                SQL(
                    f"""
                    SELECT indice FROM {{}} WHERE indice < {{}} 
                    {f'and "{where_col}" = {parent_id} ' if where_col else ''} 
                    ORDER BY indice DESC LIMIT 1;
                """
                ).format(Identifier(tablename), desired_index),
                count=1,
            )
            index_before = index_before[0] if index_before else None
        else:
            index_before = desired_index

        if current_index < desired_index:
            index_after = self.database_manager.query(
                SQL(
                    f"""
                    SELECT indice FROM {{}} WHERE indice > {{}}
                    {f'and "{where_col}" = {parent_id}' if where_col else ''}
                    ORDER BY indice LIMIT 1;
                """
                ).format(Identifier(tablename), desired_index),
                count=1,
            )

            index_after = index_after[0] if index_after else None
        else:
            index_after = desired_index

        # endregion

        if desired_element_id == element_id or desired_index == current_index:
            # If the element itself is the element after it means it's being updated to its same position so just ignore it.
            return
        elif index_before and not index_after:
            # If moved to the end set it to the next available value
            self.database_manager.query(
                SQL("UPDATE {} SET indice = DEFAULT WHERE id = {}").format(
                    Identifier(tablename), element_id
                )
            )
        elif index_after and not index_before:
            # If moved to the beginning do the regular calculation with the first index only
            final_index = index_after / 2

            try:
                self.database_manager.query(
                    SQL("UPDATE {} SET indice = {} WHERE id = {};").format(
                        Identifier(tablename), final_index, element_id
                    ),
                )
            except errors.UniqueViolation:
                # This means that the precision limit has been reached and should be refactored
                self.fix_precision_limit(tablename, final_index)
                # Insert the element again since it failed last time
                self.update_index(element_id, tablename, new_index)
        else:
            # Move the element to the desired position
            final_index = (index_before + index_after) / 2

            try:
                self.database_manager.query(
                    SQL("UPDATE {} SET indice = {} WHERE id = {};").format(
                        Identifier(tablename), final_index, element_id
                    ),
                )
            except errors.UniqueViolation:
                # This means that the precision limit has been reached and should be refactored
                self.fix_precision_limit(tablename, final_index)
                # Insert the element again since it failed last time
                self.update_index(element_id, tablename, new_index)

    def fix_precision_limit(self, tablename: str, index_range: int):
        """
        Reorganizes the indexes of the given tablename around the `index_range`.
        This is used when reordering has reached its precision limit.
        """

        upper_bound = ceil(index_range)
        lower_bound = floor(index_range)

        entries_to_update = self.database_manager.query(
            SQL(
                "SELECT id, indice FROM {} WHERE indice > {} AND indice < {} SORT BY indice;"
            ).format(Identifier(tablename), lower_bound, upper_bound),
        )

        # How much space to leave between elements to spread them evenly
        interval_between_indices = 1 / len(entries_to_update)

        for index, id in enumerate(entries_to_update, 1):
            self.database_manager.query(
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
