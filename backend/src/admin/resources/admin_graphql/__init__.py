from __future__ import annotations
import typing
import strawberry
import strawberry.file_uploads
from auth.decorators import login_required
from common.common_graphql import schemas
from common.common_graphql import enums
from admin.resources.admin_graphql import errors, inputs
from psycopg.sql import SQL, Identifier


if typing.TYPE_CHECKING:
    from admin.utilities.types import AdminResourceManager, GraphQLContext


@strawberry.type()
class Query:
    @strawberry.field(
        description="Returns all the obras ordered by index limited by page_size. Can be filtered by name."
    )
    def obras(
        self,
        info: strawberry.Info[GraphQLContext],
        page: typing.Annotated[
            int, strawberry.argument(description="The page to get.")
        ] = 1,
        page_size: typing.Annotated[
            int, strawberry.argument(description="The size of each page.")
        ] = 10,
        name: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(description="Filter obras by name."),
        ] = None,
    ) -> schemas.ObraResult:
        resource_manager = info.context["resource_manager"]
        if name:
            return resource_manager.get_obras_by_name(name, page, page_size)

        return resource_manager.get_obras(page, page_size)

    @strawberry.field(description="Returns the obra matching the given ID or null.")
    def obra(
        self,
        info: strawberry.Info[GraphQLContext],
        id: typing.Annotated[
            int, strawberry.argument(description="The ID of the obra to get.")
        ],
    ) -> typing.Optional[schemas.Obra]:
        resource_manager: AdminResourceManager = info.context["resource_manager"]
        return resource_manager.get_obra_by_id(id)

    @strawberry.field(description="Returns the ambiente matching the given ID or null.")
    def ambiente(
        self,
        info: strawberry.Info[GraphQLContext],
        id: typing.Annotated[
            int, strawberry.argument(description="The ID of ambiente to get.")
        ],
    ) -> typing.Optional[schemas.Ambiente]:
        return info.context.get("resource_manager").get_ambiente_by_id(id)

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

    @strawberry.field(description="All the images shown in the main page")
    def mainPageImages(
        self, info: strawberry.Info[GraphQLContext]
    ) -> typing.List[schemas.Image]:
        resource_manager = info.context.get("resource_manager")
        image_filenames = resource_manager.database_manager.query(
            """
            SELECT archivo from imagen JOIN imagenConfig on imagenConfig.imagen_id = imagen.id 
            WHERE imagen.pagina_principal ORDER BY imagenConfig.indice;
            """
        )

        return [
            resource_manager.get_image_by_filename(filename[0])
            for filename in image_filenames
        ]


@strawberry.type
class Mutation:
    @strawberry.mutation(description="Creates a new obra.")
    def createObra(
        self,
        info: strawberry.Info[GraphQLContext],
        name: typing.Annotated[
            str, strawberry.argument(description="The name of the new obra.")
        ],
        description: typing.Annotated[
            str,
            strawberry.argument(
                description="The description of the new obra in markdown syntax."
            ),
        ],
        area: typing.Annotated[
            int,
            strawberry.argument(
                description="The area of the new obra in square meters."
            ),
        ],
    ) -> schemas.Obra:
        return info.context["resource_manager"].create_obra(name, description, area)

    @strawberry.mutation(
        description="Deletes a given obra alongside all its ambientes and images returning the deleted data. **If null it means the obra wasn't found.**"
    )
    def deleteObra(
        self,
        info: strawberry.Info[GraphQLContext],
        id: typing.Annotated[
            int, strawberry.argument(description="The ID of the obra to delete.")
        ],
    ) -> bool:
        return info.context["resource_manager"].delete_obra(id)

    @strawberry.mutation(
        description="Updates the obra identified by ID with the given parameters. All are optional, leave blank to not update. **If null it means the obra wasn't found.**"
    )
    def updateObra(
        self,
        info: strawberry.Info[GraphQLContext],
        id: typing.Annotated[
            int, strawberry.argument(description="The ID of the obra to update.")
        ],
        name: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(description="The new name of the obra."),
        ] = None,
        description: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(
                description="The new description of the obra in markdown format."
            ),
        ] = None,
        area: typing.Annotated[
            typing.Optional[int],
            strawberry.argument(
                description="The new area of the obra in square meters."
            ),
        ] = None,
        thumbnail: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(
                description="The filename of the thumbnail to set for this obra. **Set to null to remove the thumbnail**."
            ),
        ] = strawberry.UNSET,
        index: typing.Annotated[
            typing.Optional[int],
            strawberry.argument(
                description="The zero based index of where to position the obra relative to all others."
            ),
        ] = None,
        public: typing.Annotated[
            typing.Optional[bool],
            strawberry.argument(
                description="Sets an obra to be publicly available in the public website."
            ),
        ] = None,
    ) -> typing.Optional[schemas.Obra]:
        return info.context["resource_manager"].update_obra(
            id, name, description, area, thumbnail, index, public
        )

    @strawberry.mutation(description="Creates a new ambiente.")
    def createAmbiente(
        self,
        info: strawberry.Info[GraphQLContext],
        obra_id: typing.Annotated[
            int,
            strawberry.argument(
                description="The ID of the obra this ambiente will belong to."
            ),
        ],
        name: typing.Annotated[
            str,
            strawberry.argument(description="The name of the new ambiente."),
        ],
        description: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(
                description="The description of the new ambiente in markdown format. **Can be left blank.**"
            ),
        ] = None,
    ) -> typing.Union[schemas.Ambiente, errors.ObraNotFoundAmbiente]:
        return info.context["resource_manager"].create_ambiente(
            obra_id, name, description
        )

    @strawberry.mutation(
        description="Updates the ambiente identified by id with the given parameters. All are optional. **Returns the updated data or null if no ambiente was found.**"
    )
    def updateAmbiente(
        self,
        info: strawberry.Info[GraphQLContext],
        id: typing.Annotated[
            int,
            strawberry.argument(description="The ID of the ambiente to update."),
        ],
        name: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(description="The new name of the ambiente."),
        ] = None,
        description: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(
                description="The new description of the ambiente in markdown format. ***Leave blank to remove description.**"
            ),
        ] = None,
        index: typing.Annotated[
            typing.Optional[int],
            strawberry.argument(
                description="The zero based index of where to position the ambiente relative to all others within the same obra."
            ),
        ] = None,
    ) -> typing.Optional[schemas.Ambiente]:
        resource_manager: AdminResourceManager = info.context["resource_manager"]
        return resource_manager.update_ambiente(id, name, description, index)

    @strawberry.mutation(
        description="Deletes a given ambiente alongside all its images returning the deleted data. **If null it means the ambiente wasn't found.**"
    )
    def deleteAmbiente(
        self,
        info: strawberry.Info[GraphQLContext],
        id: typing.Annotated[
            int, strawberry.argument(description="The ID of the ambiente to delete.")
        ],
    ) -> bool:
        return info.context["resource_manager"].delete_ambiente(id)

    @strawberry.mutation(
        description="Creates a a new image for the given ambiente. Returns an error if the ambiente wasn't found or the filetype isn't supported."
    )
    def createImage(
        self,
        info: strawberry.Info[GraphQLContext],
        ambiente_id: typing.Annotated[
            int,
            strawberry.argument(
                description="The ID of the ambiente this image will belong to."
            ),
        ],
        image: typing.Annotated[
            strawberry.file_uploads.Upload,
            strawberry.argument(description="The image file to upload."),
        ],
        alt_text: typing.Annotated[
            str,
            strawberry.argument(
                description="The alt text of the image. This is meant for impaired vision, not a description."
            ),
        ],
    ) -> typing.Union[
        schemas.Image, errors.AmbienteNotFoundImage, errors.UnsupportedFileType
    ]:
        return info.context["resource_manager"].create_image(
            image, alt_text, ambiente_id
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
        alt_text: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(description="The new alt text of the image."),
        ] = None,
        description: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(description="The new description of the image."),
        ] = None,
        descriptionFont: typing.Annotated[
            typing.Optional[str],
            strawberry.argument(description="The font used for the description."),
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
        phone_config: typing.Annotated[
            typing.Optional[inputs.phoneConfigInput],
            strawberry.argument(
                description="The configuration for the image display in phones."
            ),
        ] = None,
    ) -> typing.Optional[schemas.Image]:
        return info.context["resource_manager"].update_image(
            filename,
            alt_text,
            index,
            main_page,
            hide_in_project,
            description,
            descriptionFont,
            phone_config,
        )

    @strawberry.mutation(
        description="Updates an mainImageConfig to be displayed in the sites main page."
    )
    def updateImageConfig(
        self,
        info: strawberry.Info[GraphQLContext],
        id: typing.Annotated[
            int, strawberry.argument(description="The ID of the imageConfig to update.")
        ],
        image_borders: typing.Annotated[
            typing.Optional[inputs.BordersInput],
            strawberry.argument("What borders should the image have"),
        ] = None,
        description: typing.Annotated[
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
        logo_pos: typing.Annotated[
            typing.Optional[enums.Direction],
            strawberry.argument(
                description="The position of where to put the logo relative to the image."
            ),
        ] = strawberry.UNSET,
        logo_borders: typing.Annotated[
            typing.Optional[inputs.BordersInput],
            strawberry.argument("What borders should the logo have"),
        ] = None,
        description_pos: typing.Annotated[
            typing.Optional[enums.Direction],
            strawberry.argument(
                description="The position of where to put the description relative to the image."
            ),
        ] = strawberry.UNSET,
        overflow: typing.Annotated[
            typing.Optional[bool],
            strawberry.argument(
                description="Determines if the image should overflow to the edge of the screen or not."
            ),
        ] = strawberry.UNSET,
        index: typing.Annotated[
            typing.Optional[int],
            strawberry.argument(
                description="The new zero based index of where to put the image in the main page."
            ),
        ] = None,
    ) -> typing.Optional[schemas.MainImageConfig]:
        resource_manager = info.context["resource_manager"]
        image = resource_manager.database_manager.query(
            """
            SELECT 1 FROM imagenConfig WHERE id = %s;
        """,
            (id,),
            1,
        )[0]

        if image:
            if description is not None:
                resource_manager.database_manager.query(
                    """
                UPDATE imagenConfig SET descripcion = %s WHERE id = %s;
                """,
                    (description, id),
                    commit=False,
                )
            if description_en is not None:
                resource_manager.database_manager.query(
                    """
                UPDATE imagenConfig SET descripcion_en = %s WHERE id = %s;
                """,
                    (description_en, id),
                    commit=False,
                )
            if description_pos is not strawberry.UNSET:
                value = None

                if description_pos:
                    value = description_pos.value

                resource_manager.database_manager.query(
                    """
                UPDATE imagenConfig SET texto_ubicacion = %s WHERE id = %s;
                """,
                    (value, id),
                    commit=False,
                )
            if description_font:
                resource_manager.database_manager.query(
                    """
                    UPDATE imagenConfig SET descripcionTipografia = %s WHERE id = %s;
                """,
                    (description_font, id),
                    commit=False,
                )
            if description_alignment:
                resource_manager.database_manager.query(
                    """
                    UPDATE imagenConfig SET descripcionDistribucion = %s WHERE id = %s;
                """,
                    (description_alignment, id),
                    commit=False,
                )
            if description_font_size is not None:
                resource_manager.database_manager.query(
                    """
                    UPDATE imagenConfig SET descripcionTamano = %s WHERE id = %s;
                """,
                    (description_font_size, id),
                    commit=False,
                )
            if logo_pos is not strawberry.UNSET:
                value = None

                if logo_pos:
                    value = logo_pos.value

                resource_manager.database_manager.query(
                    """
                UPDATE imagenConfig SET logo_ubicacion = %s WHERE id = %s;
                """,
                    (value, id),
                    commit=False,
                )

                if overflow is not strawberry.UNSET:
                    resource_manager.database_manager.query(
                        """
                    UPDATE imagenConfig SET sangrar = %s WHERE id = %s;
                    """,
                        (overflow, id),
                        commit=False,
                    )
            if logo_borders:
                for border, direction in (
                    (logo_borders.n, "n"),
                    (logo_borders.s, "s"),
                    (logo_borders.e, "e"),
                    (logo_borders.o, "o"),
                ):
                    if border is not None:
                        resource_manager.database_manager.query(
                            SQL(
                                """
                        UPDATE imagenConfig SET {} = {} WHERE id = {};
                        """
                            ).format(Identifier(f"logo_borde_{direction}"), border, id)
                        )
            if image_borders:
                for border, direction in (
                    (image_borders.n, "n"),
                    (image_borders.s, "s"),
                    (image_borders.e, "e"),
                    (image_borders.o, "o"),
                ):
                    if border is not None:
                        resource_manager.database_manager.query(
                            SQL(
                                """
                        UPDATE imagenConfig SET {} = {} WHERE id = {};
                        """
                            ).format(
                                Identifier(f"imagen_borde_{direction}"), border, id
                            )
                        )
            if index is not None:
                # Tablename in lowercase because postgres saves imagenConfig in lowercase and
                # by doing "imagenConfig" it fails because it searches case sensitive.
                resource_manager.update_index(id, "imagenconfig", index)

            resource_manager.database_manager.commit()

            data = resource_manager.database_manager.query(
                """
                SELECT imagenConfig.id, imagenConfig.descripcion, descripcion_en, logo_ubicacion, texto_ubicacion, sangrar,
                imagen_borde_n, imagen_borde_s, imagen_borde_e, imagen_borde_o,
                logo_borde_n, logo_borde_s, logo_borde_e, logo_borde_o,
                descripcionDistribucion, descripcionTamano, imagenConfig.descripcionTipografia
                FROM imagenConfig WHERE id = %s;
                """,
                (id,),
                1,
            )

            if data:
                return schemas.MainImageConfig(
                    id=data[0],
                    description=data[1],
                    description_en=data[2],
                    logo_pos=data[3],
                    description_pos=data[4],
                    overflow=data[5],
                    image_borders=schemas.Borders(
                        n=data[6], s=data[7], e=data[8], o=data[9]
                    ),
                    logo_borders=schemas.Borders(
                        n=data[10], s=data[11], e=data[12], o=data[13]
                    ),
                    description_alignment=data[14],
                    description_font_size=data[15],
                    description_font=data[16],
                )

    @strawberry.mutation(
        description="Deletes the image identified by filename returning the deleted entry. **Returns null if no image was found.**"
    )
    def deleteImage(
        self,
        info: strawberry.Info[GraphQLContext],
        filename: typing.Annotated[
            str,
            strawberry.argument(description="The filename of the image to delete."),
        ],
    ) -> bool:
        resource_manager: AdminResourceManager = info.context["resource_manager"]
        return resource_manager.delete_image(filename)
