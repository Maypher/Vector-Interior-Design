from admin import utilities
import uuid
import os
from common.resource_manager import *
from psycopg import errors
from psycopg.sql import SQL, Identifier
from psycopg import rows
from math import ceil, floor
from common.common_graphql import schemas
from admin.resources.admin_graphql import errors as GraphqlErrors
from admin.resources.admin_graphql import inputs
from admin.db.database import AdminDatabaseManager
from common.resource_manager import ResourceManager
from strawberry import UNSET
from sanic.request import File
from strawberry import UNSET
from strawberry import Info
from admin.utilities.types import GraphQLContext
from admin.utilities import image_upload
from common.utilities.environment import dev_mode


class AdminResourceManager(ResourceManager):
    def __init__(self, database_manager: AdminDatabaseManager):
        self.database_manager = database_manager
        self.allow_private = True

    def create_project(
        self, name: str, description_es: str, description_en: str, area: int
    ) -> schemas.Project:
        """Creates a new project. Data validation is assumed."""
        project_data = self.database_manager.query(
            """
        INSERT INTO project (name, description_es, description_en, area) VALUES (%s, %s, %s, %s) RETURNING *;
        """,
            (name, description_es, description_en, area),
            1,
        )

        return schemas.Project(**project_data)

    def delete_project(self, id: int, info: Info[GraphQLContext]) -> bool:
        """
        Deletes the project identified by id alongside its related spaces and images.
        """
        project = self.get_project_by_id(id)

        if not project:
            return False

        for space in project.spaces(info):
            for image in space.images(info):
                self.delete_image(image.filename)

        self.database_manager.query(
            """
        DELETE FROM project WHERE id = %s;
        """,
            (id,),
        )

        return True

    def update_project(
        self,
        id: int,
        name: str | None = None,
        description_es: str | None = None,
        description_en: str | None = None,
        area: int | None = None,
        thumbnail: int | None = UNSET,
        index: int | None = None,
        public: bool | None = None,
    ) -> typing.Optional[schemas.Image]:
        """
        Updates the project identified by id returning the updated project or `None` if no project was found.

        :param id: The id of the project to change.
        :param name: The new name of the project.
        :param description: The new description of the project.
        :param area: The area of the project in meters squared.
        :param thumbnail: The id of the image that should be the thumbnail of this project. Set to `None` to remove it.
        :param index: The new index of the project. Used to show the projects in order in the UI.
        """

        project = self.get_project_by_id(id)

        if not project:
            return

        # Done in a different step from all the rest since NULL is a possible value
        if thumbnail is not UNSET:
            try:
                self.database_manager.query(
                    """
                    UPDATE project SET main_image = %s WHERE id = %s;
                """,
                    (thumbnail, id),
                    commit=False,
                )
            except errors.DatabaseError as e:
                if e.sqlstate == "P0001":
                    return
                raise e
        if index is not None:
            self.update_index(id, "project", index)

        return self.database_manager.query(
            """
                UPDATE project SET 
                name = COALESCE(%s, name),
                description_es = COALESCE(%s, description_es),
                description_en = COALESCE(%s, description_en),
                area = COALESCE(%s, area),
                public = COALESCE(%s, public)
                WHERE id = %s RETURNING *;
            """,
            (name, description_es, description_en, area, public, id),
            count=1,
            row_factory=rows.class_row(schemas.Project),
        )

    def create_space(
        self,
        project_id: int,
        name: str,
        description_es: typing.Optional[str],
        description_en: typing.Optional[str],
    ) -> typing.Optional[schemas.Space]:
        """Creates a new space for the given project"""

        project = self.get_project_by_id(project_id)

        if not project:
            return GraphqlErrors.ProjectNotFoundSpace(project_id=project_id)

        space = self.database_manager.query(
            """
        INSERT INTO space (name, description_es, description_en, project_id) VALUES (%s, %s, %s, %s) RETURNING *;
        """,
            (name, description_es, description_en, project_id),
            1,
        )

        return schemas.Space(**space)

    def update_space(
        self,
        id: int,
        new_name: str | None = None,
        new_description_es: str | None = None,
        new_description_en: str | None = None,
        new_index: int | None = None,
    ):
        """
        Updates the space identified by id. Name and description can be updated.

        :param id: The id of the space to change.
        :param new_name: The new name of the space.
        :param description: The new description of the space.
        :param index: The new zero-based index of the space inside the project.
        """
        space = self.get_space_by_id(id)
        logger.debug(new_description_en)

        if not space:
            return

        self.database_manager.query(
            """
                UPDATE space SET 
                name = COALESCE(%s, name),
                description_es = COALESCE(%s, description_es),
                description_en = COALESCE(%s, description_en)
                WHERE id = %s;
            """,
            (new_name, new_description_es, new_description_en, id),
            commit=False,
        )

        if new_index is not None:
            project_id = self.database_manager.query(
                """
            SELECT project_id FROM space WHERE id = %s;
            """,
                (space.id,),
                count=1,
                row_factory=rows.scalar_row,
            )

            self.update_index(id, "space", new_index, "project_id", project_id)

        self.database_manager.commit()
        return self.get_space_by_id(id)

    def delete_space(self, id: int, info: Info[GraphQLContext]) -> bool:
        """
        Deletes the space identified by id alongside all images related to it.
        """
        space = self.get_space_by_id(id)

        if not space:
            return False

        # Image are collated in database but they also need to be removed from the filesystem
        for image in space.images(info):
            self.delete_image(image.filename)

        self.database_manager.query(
            """
        DELETE FROM space WHERE id = %s;
        """,
            (id,),
        )

        return True

    async def create_image(
        self,
        image: File,
        alt_text_es: str,
        alt_text_en: str,
        space_id: int,
    ) -> typing.Union[
        schemas.Image,
        GraphqlErrors.UnsupportedFileType,
        GraphqlErrors.SpaceNotFoundImage,
    ]:
        """
        Saves an image to disk relating it to the given space and returns the created Image.
        Returns an error if image is unsupported or if space doesn't exist.
        """

        if not utilities.verify_file(image.type):
            self.database_manager.rollback()
            return GraphqlErrors.UnsupportedFileType(filetype=image.type)

        space = self.get_space_by_id(space_id)

        if not space:
            return GraphqlErrors.SpaceNotFoundImage(space_id=space_id)

        image_filename = None

        if dev_mode:
            image_filename = await image_upload.upload_locally(image)
        else:
            image_filename = image_upload.upload_to_cdn(image)

        data = self.database_manager.query(
            """
        INSERT INTO image (filename, alt_text_es, alt_text_en, space_id) VALUES (%s, %s, %s, %s)
        RETURNING *;
        """,
            (image_filename, alt_text_es, alt_text_en, space.id),
            count=1,
        )

        return schemas.Image(**data)

    def update_image(
        self,
        filename: str,
        alt_text_es: str | None = None,
        alt_text_en: str | None = None,
        bg_color: str | None = None,
        new_index: int | None = None,
        main_page: bool | None = None,
        hide_in_project: bool | None = None,
        description_es: str | None = None,
        description_en: str | None = None,
        description_font: str | None = None,
        sculpture: bool | None = None,
        phone_config: inputs.PhoneConfigInput | None = None,
        desktop_config: inputs.DesktopConfigInput | None = None,
    ) -> typing.Optional[schemas.Image]:
        # TODO: Add update to desktop_config
        """
        Updates the alt text of the given image.

        :param filename: The filename of the image to update.
        :param alt_text: The new alt text of the image.
        :param new_index: The zero-based index where to move the image to.
        :param main_page: Indicates wether an image should be shown in the main page.
        :param hide_in_project: Indicates wether an image should be hidden in the project page.
        :param description: The description of the image. Shown in the project page.
        :param description_font: The font used in the description.
        :param phone_config: The configuration to display an image in the project page in mobile devices.
        """

        image = self.database_manager.query(
            """SELECT id, space_id FROM image WHERE filename = %s""", (filename,), 1
        )

        if not image:
            return

        image_id = image["id"]

        self.database_manager.query(
            f"""
                UPDATE image 
                SET alt_text_es = COALESCE(%s, alt_text_es),
                alt_text_en = COALESCE(%s, alt_text_en),
                main_page = COALESCE(%s, main_page),
                hide_in_project = COALESCE(%s, hide_in_project),
                description_es = COALESCE(%s, description_es),
                description_en = COALESCE(%s, description_en),
                description_font = COALESCE(%s, description_font),
                sculpture =  COALESCE(%s, sculpture),
                phone_config = ROW(
                COALESCE(%s, (phone_config).borders), 
                COALESCE(%s, (phone_config).alignment), 
                {"%s" if phone_config and phone_config.description_pos != UNSET else "COALESCE(%s, (phone_config).description_position)"}, 
                COALESCE(%s, (phone_config).description_alignment)
                )::image_phone_config,
                desktop_config = ROW(
                {"%s" if desktop_config and desktop_config.group_alignment != UNSET else "COALESCE(%s, (desktop_config).group_alignment)"},
                    COALESCE(%s, (desktop_config).group_end),
                    COALESCE(%s, (desktop_config).image_size),
                    COALESCE(%s, (desktop_config).image_borders),
                    {"%s" if desktop_config and desktop_config.description_position != UNSET else "COALESCE(%s, (desktop_config).description_position)"},
                    COALESCE(%s, (desktop_config).description_alignment),
                    COALESCE(%s, (desktop_config).description_borders),
                    COALESCE(%s, (desktop_config).description_logo_position),
                    COALESCE(%s, (desktop_config).logo_position),
                    COALESCE(%s, (desktop_config).logo_borders)
                )::image_desktop_config,
                bg_color = COALESCE(%s, bg_color)
                WHERE id = %s
                """,
            (
                alt_text_es,
                alt_text_en,
                main_page,
                hide_in_project,
                description_es,
                description_en,
                description_font,
                sculpture,
                (
                    phone_config.borders.to_bits()
                    if getattr(phone_config, "borders", None)
                    else None
                ),
                getattr(phone_config, "alignment", None),
                (
                    phone_config.description_pos
                    if getattr(phone_config, "description_pos", UNSET) != UNSET
                    else None
                ),
                getattr(phone_config, "description_alignment", None),
                getattr(desktop_config, "group_alignment", None),
                getattr(desktop_config, "group_end", None),
                getattr(desktop_config, "image_size", None),
                (
                    desktop_config.image_borders.to_bits()
                    if getattr(desktop_config, "image_borders", None)
                    else None
                ),
                (
                    desktop_config.description_position
                    if getattr(desktop_config, "description_position", UNSET) != UNSET
                    else None
                ),
                getattr(desktop_config, "description_alignment", None),
                (
                    desktop_config.description_borders.to_bits()
                    if getattr(desktop_config, "description_borders", None)
                    else None
                ),
                (
                    desktop_config.description_logo_position
                    if getattr(desktop_config, "description_logo_position", UNSET)
                    != UNSET
                    else None
                ),
                (
                    desktop_config.logo_position
                    if getattr(desktop_config, "logo_position", UNSET) != UNSET
                    else None
                ),
                (
                    desktop_config.logo_borders.to_bits()
                    if getattr(desktop_config, "logo_borders", None)
                    else None
                ),
                bg_color,
                image_id,
            ),
            commit=False,
        )

        if main_page:
            # Try to create a new main_page_config for the image.
            # If it already exists (UNIQUE constraint on image_id) then don't create it.
            self.database_manager.query(
                """
            INSERT INTO main_page_config (image_id) VALUES (%s) ON CONFLICT DO NOTHING;
            """,
                (image_id,),
            )

        if sculpture:
            # Try to create a new sculpture_data for the image.
            # If it already exists (UNIQUE constraint on image_id) then don't create it.
            self.database_manager.query(
                """
            INSERT INTO sculpture_data (image_id) VALUES (%s) ON CONFLICT DO NOTHING;
            """,
                (image_id,),
            )

        if new_index is not None:
            self.update_index(
                image_id, "image", new_index, "space_id", image["space_id"]
            )

        self.database_manager.commit()
        return self.get_image_by_filename(filename)

    def delete_image(self, filename: str) -> bool:
        """Deletes the given image from the database and file system."""

        image = self.get_image_by_filename(filename)

        if not image:
            return False

        if dev_mode:
            location = f"{image_upload.STORAGE_LOCATION}{filename}"
            if os.path.exists(location):
                os.remove(location)
            else:
                return False
        else:
            image_upload.delete_from_cdn(filename)

        self.database_manager.query(
            """
            DELETE FROM image WHERE filename = %s;
            """,
            (filename,),
        )
        return True

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
        :param where_col: For spaces and images. Used to filter by project/space.
        :param parent_id: The id of the element to filter `where_col` by.
        """

        max_index = self.database_manager.query(
            SQL(
                f"SELECT COUNT(*) FROM {{}} {SQL("WHERE {} = {}".format(Identifier(where_col), parent_id)) if where_col else ''};"
            ).format(Identifier(tablename)),
            count=1,
            row_factory=rows.scalar_row,
        )

        # Clamp the new index between 0 and max index
        # -1 because postgres offsets exclude the given value so offset 3 would remove 3 values and give the 4th
        new_index = min(max(new_index, 0), int(max_index) - 1)

        # region get indices of elements around the selected one

        # The index of the element before being updated
        current_index = self.database_manager.query(
            SQL(
                f"""
            SELECT index FROM {{}} WHERE {f' "{where_col}" = {parent_id} and' if where_col else ''} id = {{}};
        """
            ).format(Identifier(tablename), element_id),
            count=1,
            row_factory=rows.scalar_row,
        )

        # Transform the index from zero based to the database float version
        desired_pos_data = self.database_manager.query(
            SQL(
                f"""
            SELECT id, index FROM {{}} {f'WHERE "{where_col}" = {parent_id}' if where_col else ''} ORDER BY index OFFSET {{}} LIMIT 1; 
            """,
            ).format(Identifier(tablename), new_index),
            count=1,
        )

        desired_element_id = desired_pos_data["id"] if desired_pos_data else None
        desired_index = desired_pos_data["index"] if desired_pos_data else None

        if current_index > desired_index:
            index_before = self.database_manager.query(
                SQL(
                    f"""
                    SELECT index FROM {{}} WHERE index < {{}} 
                    {f'AND "{where_col}" = {parent_id} ' if where_col else ''} 
                    ORDER BY index DESC LIMIT 1;
                """
                ).format(Identifier(tablename), desired_index),
                count=1,
            )
            index_before = index_before["index"] if index_before else None
        else:
            index_before = desired_index

        if current_index < desired_index:
            index_after = self.database_manager.query(
                SQL(
                    f"""
                    SELECT index FROM {{}} WHERE index > {{}}
                    {f'AND "{where_col}" = {parent_id}' if where_col else ''}
                    ORDER BY index LIMIT 1;
                """
                ).format(Identifier(tablename), desired_index),
                count=1,
            )

            index_after = index_after["index"] if index_after else None
        else:
            index_after = desired_index

        # endregion

        if desired_element_id == element_id or desired_index == current_index:
            # If the element itself is the element after it means it's being updated to its same position so just ignore it.
            return
        elif index_before and not index_after:
            # If moved to the end set it to the next available value
            self.database_manager.query(
                SQL("UPDATE {} SET index = DEFAULT WHERE id = {}").format(
                    Identifier(tablename), element_id
                )
            )
        elif index_after and not index_before:
            # If moved to the beginning do the regular calculation with the first index only
            final_index = index_after / 2

            try:
                self.database_manager.query(
                    SQL("UPDATE {} SET index = {} WHERE id = {};").format(
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
                    SQL("UPDATE {} SET index = {} WHERE id = {};").format(
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
                "SELECT id, index FROM {} WHERE index > {} AND index < {} SORT BY index;"
            ).format(Identifier(tablename), lower_bound, upper_bound),
        )

        # How much space to leave between elements to spread them evenly
        interval_between_indices = 1 / len(entries_to_update)

        for index, id in enumerate(entries_to_update, 1):
            self.database_manager.query(
                SQL(
                    """
                UPDATE {} SET index = {} = {} WHERE id = {};
                """
                ).format(
                    Identifier(tablename),
                    lower_bound + interval_between_indices * index,
                    id,
                ),
            )

    def update_main_page_image_config(
        self,
        id: int,
        description_es: typing.Optional[str] = None,
        description_en: typing.Optional[str] = None,
        description_font: typing.Optional[str] = None,
        description_font_size: typing.Optional[float] = None,
        description_alignment: typing.Optional[str] = None,
        bg_color: typing.Optional[str] = None,
        phone_config: typing.Optional[inputs.MainPageImagePhoneConfigInput] = None,
        desktop_config: typing.Optional[inputs.MainPageImageDesktopConfigInput] = None,
        index: typing.Optional[int] = None,
    ) -> schemas.MainPageImageConfig:
        """
        Updates the configuration of an image that is shown in the main page of the site.

        :param id: The `id` of the `main_page_config` to update.
        :param description_es: The description of the image in Spanish.
        :param description_en: The description of the image in English.
        :param description_font: The font of the description.
        :param description_font_size: The font size of the description.
        :param description_alignment: The alignment of the description. It's any of tailwind's text-align values.
        :param phone_config: An input of type `mainPagePhoneConfig` that includes all data related to the mobile display of the main screen.
        :param index: The zero-based index of the image. Used for UI ordering.
        """
        main_page_config = self.database_manager.query(
            """
            SELECT 1 FROM main_page_config WHERE id = %s;
        """,
            (id,),
            1,
            row_factory=rows.tuple_row,
        )[0]

        if not main_page_config:
            return

        if phone_config:
            # Done this way rather than updating with everything else since
            # description_position and logo_position being null means they should be hidden
            # And doing logo_position if logo_position else None will always set it even
            # if it isn't passed.
            self.database_manager.query(
                """
                UPDATE main_page_config SET
                phone_config.image_borders = COALESCE(%s, (phone_config).image_borders),
                phone_config.logo_borders = COALESCE(%s, (phone_config).logo_borders),
                phone_config.overflow = COALESCE(%s, (phone_config).overflow)
                WHERE id = %s;
            """,
                (
                    (
                        phone_config.image_borders.to_bits()
                        if phone_config.image_borders
                        else None
                    ),
                    (
                        phone_config.logo_borders.to_bits()
                        if phone_config.logo_borders
                        else None
                    ),
                    phone_config.overflow,
                    id,
                ),
                commit=False,
            )

            if phone_config.description_position is not UNSET:
                self.database_manager.query(
                    """
                    UPDATE main_page_config SET
                    phone_config.description_position = %s
                    WHERE id = %s;
                """,
                    (phone_config.description_position, id),
                    commit=False,
                )
            if phone_config.logo_position is not UNSET:
                self.database_manager.query(
                    """
                    UPDATE main_page_config SET
                    phone_config.logo_position = %s
                    WHERE id = %s;
                """,
                    (phone_config.logo_position, id),
                    commit=False,
                )

        if desktop_config:
            self.database_manager.query(
                """
                UPDATE main_page_config SET
                desktop_config.image_position = COALESCE(%s, (desktop_config).image_position),
                desktop_config.description_borders = COALESCE(%s, (desktop_config).description_borders),
                desktop_config.logo_borders = COALESCE(%s, (desktop_config).logo_borders),
                desktop_config.description_logo_borders = COALESCE(%s, (desktop_config).description_logo_borders),
                desktop_config.overflow = COALESCE(%s, (desktop_config).overflow)
                WHERE id = %s;
            """,
                (
                    desktop_config.image_position,
                    (
                        desktop_config.description_borders.to_bits()
                        if desktop_config.description_borders
                        else None
                    ),
                    (
                        desktop_config.logo_borders.to_bits()
                        if desktop_config.logo_borders
                        else None
                    ),
                    (
                        desktop_config.description_logo_borders.to_bits()
                        if desktop_config.description_logo_borders
                        else None
                    ),
                    desktop_config.overflow,
                    id,
                ),
                commit=False,
            )

            if desktop_config.description_position is not UNSET:
                self.database_manager.query(
                    """
                    UPDATE main_page_config SET
                    desktop_config.description_position = %s
                    WHERE id = %s;
                    """,
                    (desktop_config.description_position, id),
                    commit=False,
                )
            if desktop_config.logo_position is not UNSET:
                self.database_manager.query(
                    """
                    UPDATE main_page_config SET
                    desktop_config.logo_position = %s
                    WHERE id = %s;
                    """,
                    (desktop_config.logo_position, id),
                    commit=False,
                )
            if desktop_config.description_logo_position is not UNSET:
                self.database_manager.query(
                    """
                    UPDATE main_page_config SET
                    desktop_config.description_logo_position = %s
                    WHERE id = %s;
                """,
                    (desktop_config.description_logo_position, id),
                )

        if index is not None:
            self.update_index(id, "main_page_config", index)

        return self.database_manager.query(
            """
            UPDATE main_page_config SET 
            description_es = COALESCE(%s, description_es),
            description_en = COALESCE(%s, description_en),
            description_font = COALESCE(%s, description_font),
            description_font_size = COALESCE(%s, description_font_size),
            description_alignment = COALESCE(%s, description_alignment),
            bg_color = COALESCE(%s, bg_color)
            WHERE id = %s RETURNING *;
            """,
            (
                description_es,
                description_en,
                description_font,
                description_font_size,
                description_alignment,
                bg_color,
                id,
            ),
            count=1,
            row_factory=rows.class_row(schemas.MainPageImageConfig),
        )

    def update_sculpture_data(
        self,
        id: int,
        description_es: typing.Optional[str],
        description_en: typing.Optional[str],
        bg_color: typing.Optional[str],
        index: typing.Optional[int],
    ) -> schemas.SculptureData:
        """
        Updates the configuration of an image that is shown as a sculpture returning
        the updated data or null if no data was found.

        :param id: The `id` of the `sculpture_data` to update.
        :param description_es: The description of the sculpture in Spanish.
        :param description_en: The description of the sculpture in English.
        :param index: The index for ordering the sculptures relative to each other.
        """
        sculpture_data = self.database_manager.query(
            """
            SELECT 1 FROM sculpture_data WHERE id = %s;
        """,
            (id,),
            1,
            row_factory=rows.tuple_row,
        )[0]

        if not sculpture_data:
            return

        if index is not None:
            self.update_index(id, "sculpture_data", index)

        return self.database_manager.query(
            """
            UPDATE sculpture_data SET 
            description_es = COALESCE(%s, description_es),
            description_en = COALESCE(%s, description_en),
            bg_color = COALESCE(%s, bg_color)
            WHERE id = %s RETURNING *;
            """,
            (description_es, description_en, bg_color, id),
            count=1,
            row_factory=rows.class_row(schemas.SculptureData),
        )
