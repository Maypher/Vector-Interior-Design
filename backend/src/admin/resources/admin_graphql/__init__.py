from __future__ import annotations
import typing
import strawberry
import strawberry.file_uploads
from common.common_graphql import schemas
from admin.resources.admin_graphql import errors, inputs
from sanic.log import logger
from psycopg import rows

if typing.TYPE_CHECKING:
    from admin.utilities.types import AdminResourceManager, GraphQLContext


@strawberry.type()
class Query:
    @strawberry.field(
        description="Returns all the projects ordered by index. Can be filtered by name."
    )
    def projects(
        self,
        info: strawberry.Info[GraphQLContext],
        name: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(description="Filter projects by name."),
        ] = None,
    ) -> list[schemas.Project]:
        resource_manager = info.context["resource_manager"]
        if name is not None:
            return resource_manager.get_projects_by_name(name)

        return resource_manager.get_projects()

    @strawberry.field(description="Returns the project matching the given ID or null.")
    def project(
        self,
        info: strawberry.Info[GraphQLContext],
        id: typing.Annotated[
            int, strawberry.argument(description="The ID of the project to get.")
        ],
    ) -> typing.Optional[schemas.Project]:
        return info.context["resource_manager"].get_project_by_id(id)

    @strawberry.field(description="Returns the space matching the given ID or null.")
    def space(
        self,
        info: strawberry.Info[GraphQLContext],
        id: typing.Annotated[
            int, strawberry.argument(description="The ID of space to get.")
        ],
    ) -> typing.Optional[schemas.Space]:
        return info.context.get("resource_manager").get_space_by_id(id)

    @strawberry.field(
        description="Returns the image matching the given filename or null."
    )
    def image(
        self,
        info: strawberry.Info[GraphQLContext],
        filename: typing.Annotated[
            str, strawberry.argument(description="The filename of the image to get.")
        ],
    ) -> typing.Optional[schemas.Image]:
        return info.context.get("resource_manager").get_image_by_filename(filename)

    @strawberry.field(description="All the images shown in the main page.")
    def mainPageImages(
        self, info: strawberry.Info[GraphQLContext]
    ) -> typing.List[schemas.Image]:
        resource_manager = info.context.get("resource_manager")
        return resource_manager.database_manager.query(
            """
            SELECT image.* FROM image JOIN main_page_config on main_page_config.image_id = image.id 
            WHERE image.main_page ORDER BY main_page_config.index;
            """,
            row_factory=rows.class_row(schemas.Image),
        )

    @strawberry.field(description="All the sculptures.")
    def sculptures(self, info: strawberry.Info[GraphQLContext]) -> list[schemas.Image]:
        return info.context.get("resource_manager").database_manager.query(
            "SELECT image.* FROM image JOIN sculpture_data ON sculpture_data.image_id = image.id WHERE image.sculpture ORDER BY sculpture_data.index;",
            row_factory=rows.class_row(schemas.Image),
        )


@strawberry.type
class Mutation:
    @strawberry.mutation(description="Creates a new project.")
    def createProject(
        self,
        info: strawberry.Info[GraphQLContext],
        name: typing.Annotated[
            str, strawberry.argument(description="The name of the new project.")
        ],
        description_es: typing.Annotated[
            str,
            strawberry.argument(
                description="The description of the new project in Spanish."
            ),
        ],
        description_en: typing.Annotated[
            str,
            strawberry.argument(
                description="The description of the new project in English."
            ),
        ],
        area: typing.Annotated[
            int,
            strawberry.argument(
                description="The area of the new project in square meters."
            ),
        ],
    ) -> schemas.Project:
        return info.context["resource_manager"].create_project(
            name, description_es, description_en, area
        )

    @strawberry.mutation(
        description="Deletes a given project alongside all its spaces and images. Returns a boolean indicating if the project was successfully deleted."
    )
    def deleteProject(
        self,
        info: strawberry.Info[GraphQLContext],
        id: typing.Annotated[
            int, strawberry.argument(description="The ID of the project to delete.")
        ],
    ) -> bool:
        return info.context["resource_manager"].delete_project(id, info)

    @strawberry.mutation(
        description="Updates the project identified by ID with the given parameters. All are optional, leave blank to not update. **If null it means the project wasn't found.**"
    )
    def updateProject(
        self,
        info: strawberry.Info[GraphQLContext],
        id: typing.Annotated[
            int, strawberry.argument(description="The ID of the project to update.")
        ],
        name: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(description="The new name of the project."),
        ] = None,
        description_es: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(
                description="The new description of the project in Spanish in markdown format."
            ),
        ] = None,
        description_en: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(
                description="The new description in English in markdown format"
            ),
        ] = None,
        area: typing.Annotated[
            typing.Optional[int],
            strawberry.argument(
                description="The new area of the project in square meters."
            ),
        ] = None,
        thumbnail: typing.Annotated[
            typing.Optional[int],
            strawberry.argument(
                description="The id of the thumbnail to set for this project. **Set to null to remove the thumbnail**."
            ),
        ] = strawberry.UNSET,
        index: typing.Annotated[
            typing.Optional[int],
            strawberry.argument(
                description="The zero based index of where to position the project relative to all others."
            ),
        ] = None,
        public: typing.Annotated[
            typing.Optional[bool],
            strawberry.argument(
                description="Sets an project to be publicly available in the public website."
            ),
        ] = None,
    ) -> typing.Optional[schemas.Project]:
        return info.context["resource_manager"].update_project(
            id, name, description_es, description_en, area, thumbnail, index, public
        )

    @strawberry.mutation(description="Creates a new space.")
    def createSpace(
        self,
        info: strawberry.Info[GraphQLContext],
        project_id: typing.Annotated[
            int,
            strawberry.argument(
                description="The ID of the project this space will belong to."
            ),
        ],
        name: typing.Annotated[
            str,
            strawberry.argument(description="The name of the new space."),
        ],
        description_es: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(
                description="The description of the new space in Spanish markdown format. **Can be left blank.**"
            ),
        ] = None,
        description_en: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(
                description="The description of the new space in English markdown format. **Can be left blank.**"
            ),
        ] = None,
    ) -> typing.Union[schemas.Space, errors.ProjectNotFoundSpace]:
        return info.context["resource_manager"].create_space(
            project_id, name, description_es, description_en
        )

    @strawberry.mutation(
        description="Updates the space identified by id with the given parameters. All are optional. **Returns the updated data or null if no space was found.**"
    )
    def updateSpace(
        self,
        info: strawberry.Info[GraphQLContext],
        id: typing.Annotated[
            int,
            strawberry.argument(description="The ID of the space to update."),
        ],
        name: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(description="The new name of the space."),
        ] = None,
        description_es: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(
                description="The new description of the space in Spanish markdown format. ***Leave blank to remove description.**"
            ),
        ] = None,
        description_en: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(
                description="The new description of the space in English markdown format. ***Leave blank to remove description.**"
            ),
        ] = None,
        index: typing.Annotated[
            typing.Optional[int],
            strawberry.argument(
                description="The zero based index of where to position the space relative to all others within the same project."
            ),
        ] = None,
    ) -> typing.Optional[schemas.Space]:
        resource_manager: AdminResourceManager = info.context["resource_manager"]
        return resource_manager.update_space(
            id, name, description_es, description_en, index
        )

    @strawberry.mutation(
        description="Deletes a given space alongside all its images returning the deleted data. **If null it means the space wasn't found.**"
    )
    def deleteSpace(
        self,
        info: strawberry.Info[GraphQLContext],
        id: typing.Annotated[
            int, strawberry.argument(description="The ID of the space to delete.")
        ],
    ) -> bool:
        return info.context["resource_manager"].delete_space(id, info)

    @strawberry.mutation(
        description="Creates a a new image for the given space. Returns an error if the space wasn't found or the filetype isn't supported."
    )
    async def createImage(
        self,
        info: strawberry.Info[GraphQLContext],
        space_id: typing.Annotated[
            int,
            strawberry.argument(
                description="The ID of the space this image will belong to."
            ),
        ],
        image: typing.Annotated[
            strawberry.file_uploads.Upload,
            strawberry.argument(description="The image file to upload."),
        ],
        alt_text_es: typing.Annotated[
            str,
            strawberry.argument(
                description="The alt text of the image. This is meant for impaired vision, not a description."
            ),
        ],
        alt_text_en: typing.Annotated[
            str,
            strawberry.argument(
                description="The alt text of the image in English. This is meant for impaired vision, not a description."
            ),
        ],
    ) -> typing.Union[
        schemas.Image, errors.SpaceNotFoundImage, errors.UnsupportedFileType
    ]:
        return await info.context["resource_manager"].create_image(
            image, alt_text_es, alt_text_en, space_id
        )

    @strawberry.mutation(
        description="Updates the image identified by filename. All parameters are optional. **Returns the updated image or null if no image was found.**"
    )
    def updateImage(
        self,
        info: strawberry.Info[GraphQLContext],
        filename: typing.Annotated[
            str, strawberry.argument(description="The filename of the image to update.")
        ],
        alt_text_es: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(
                description="The new alt text of the image in Spanish."
            ),
        ] = None,
        alt_text_en: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(
                description="The new alt text of the image in English."
            ),
        ] = None,
        description_es: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(
                description="The new description of the image in Spanish."
            ),
        ] = None,
        description_en: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(
                description="The new description of the image in English."
            ),
        ] = None,
        description_font: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(description="The font used for the description."),
        ] = None,
        bg_color: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(
                description="The color used in the background in hex format (include #)."
            ),
        ] = None,
        index: typing.Annotated[
            typing.Optional[int],
            strawberry.argument(
                description="The zero based index of where to position the image relative to all others."
            ),
        ] = None,
        main_page: typing.Annotated[
            typing.Optional[bool],
            strawberry.argument(
                description="Set this image to be shown in the main page."
            ),
        ] = None,
        hide_in_project: typing.Annotated[
            typing.Optional[bool],
            strawberry.argument(description="Hide this image in the project."),
        ] = None,
        sculpture: typing.Annotated[
            typing.Optional[bool],
            strawberry.argument(description="Indicates that this image is a sculpture"),
        ] = None,
        phone_config: typing.Annotated[
            typing.Optional[inputs.PhoneConfigInput],
            strawberry.argument(
                description="The configuration for the image display in phones."
            ),
        ] = None,
        desktop_config: typing.Annotated[
            typing.Optional[inputs.DesktopConfigInput],
            strawberry.argument("The configuration for the image display in desktop."),
        ] = None,
    ) -> typing.Optional[schemas.Image]:
        return info.context["resource_manager"].update_image(
            filename,
            alt_text_es,
            alt_text_en,
            bg_color,
            index,
            main_page,
            hide_in_project,
            description_es,
            description_en,
            description_font,
            sculpture,
            phone_config,
            desktop_config,
        )

    @strawberry.mutation(
        description="Deletes the image identified by filename returning the deleted entry. **Returns null if no image was found.**"
    )
    async def deleteImage(
        self,
        info: strawberry.Info[GraphQLContext],
        filename: typing.Annotated[
            str,
            strawberry.argument(description="The filename of the image to delete."),
        ],
    ) -> bool:
        resource_manager: AdminResourceManager = info.context["resource_manager"]
        return await resource_manager.delete_image(filename)

    @strawberry.mutation(
        description="Updates the config of an image to be displayed in the site's main page."
    )
    def updateMainPageConfig(
        self,
        info: strawberry.Info[GraphQLContext],
        id: typing.Annotated[
            int,
            strawberry.argument(
                description="The ID of the main_page_config to update."
            ),
        ],
        description_es: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(description="The description of the image in Spanish."),
        ] = None,
        description_en: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(description="The description of the image in English"),
        ] = None,
        description_font: typing.Annotated[
            typing.Optional[str],
            strawberry.argument("The font that should be used for the description"),
        ] = None,
        description_alignment: typing.Annotated[
            typing.Optional[str],
            strawberry.argument("The alignment of the description"),
        ] = None,
        description_font_size: typing.Annotated[
            typing.Optional[float],
            strawberry.argument("The size used for the description in rem units"),
        ] = None,
        bg_color: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(
                "The color used in the background in hex format (include #)."
            ),
        ] = None,
        image_size: typing.Annotated[
            typing.Optional[int],
            strawberry.argument(
                "The relative size of the image in its container in a range of 0-100."
            ),
        ] = None,
        index: typing.Annotated[
            typing.Optional[int],
            strawberry.argument(
                description="The new zero based index of where to put the image in the main page."
            ),
        ] = None,
        phone_config: typing.Annotated[
            typing.Optional[inputs.MainPageImagePhoneConfigInput],
            strawberry.argument(
                description="The configuration for how the image will look in mobile devices."
            ),
        ] = None,
        desktop_config: typing.Annotated[
            typing.Optional[inputs.MainPageImageDesktopConfigInput],
            strawberry.argument(
                description="The configuration for how the image will look on desktop devices."
            ),
        ] = None,
    ) -> typing.Optional[schemas.MainPageImageConfig]:
        return info.context["resource_manager"].update_main_page_image_config(
            id,
            description_es,
            description_en,
            description_font,
            description_font_size,
            description_alignment,
            bg_color,
            image_size,
            phone_config,
            desktop_config,
            index,
        )

    @strawberry.mutation(description="Update a sculpture's data.")
    def updateSculptureData(
        self,
        info: strawberry.Info[GraphQLContext],
        id: typing.Annotated[
            int,
            strawberry.argument(
                description="The id of the `sculpture_data` to update."
            ),
        ],
        description_es: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(
                description="The description of the sculpture in Spanish."
            ),
        ] = None,
        description_en: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(
                description="The description of the sculpture in English."
            ),
        ] = None,
        bg_color: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(
                description="The color used in the background in hex format (include #)."
            ),
        ] = None,
        index: typing.Annotated[
            typing.Optional[int],
            strawberry.argument(
                description="The zero-based index of the new position of the sculpture relative to all others."
            ),
        ] = None,
    ) -> schemas.SculptureData:
        return info.context["resource_manager"].update_sculpture_data(
            id, description_es, description_en, bg_color, index
        )
