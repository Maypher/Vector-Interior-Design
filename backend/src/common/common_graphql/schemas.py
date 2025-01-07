import typing
import strawberry
from common.common_graphql import enums
from common.types import ResourceInfo


@strawberry.type(description="The main structure of the database.")
class Obra:
    id: int = strawberry.field(description="The ID of the obra in the database.")
    name: str = strawberry.field(description="The name of the obra.")
    description: str = strawberry.field(
        description="The description of the obra written in markdown format."
    )
    area: int = strawberry.field(description="The area of the obra in meters squared.")
    index: float = strawberry.field(
        description="The index of the obra for UI ordering purposes. It's a float due to how the database handles reordering."
    )
    public: bool = strawberry.field(
        description="Indicates if the obra is available in the public end of the website."
    )

    @strawberry.field(
        description="An obra can have a thumbnail that will be the first thing shown in the UI."
    )
    def thumbnail(self, info: ResourceInfo) -> typing.Optional["Image"]:
        image_data = info.context["resource_manager"].database_manager.query(
            """
            SELECT imagen.id, archivo, texto_alt, imagen.indice, pagina_principal, imagen.descripcion, 
            imagen.descripcionTipografia, esconderEnObra FROM imagen 
            JOIN obra ON obra.imagen_principal = imagen.id
            WHERE obra.id = %s;
        """,
            (self.id,),
            1,
        )

        if image_data:
            image_id = image_data[0]
            filename = image_data[1]
            alt_text = image_data[2]
            image_index = image_data[3]
            main_page = image_data[4]
            description = image_data[5]
            description_font = image_data[6]
            hide_in_project = image_data[7]

            return Image(
                id=image_id,
                filename=filename,
                alt_text=alt_text,
                index=image_index,
                main_page=main_page,
                description=description,
                description_font=description_font,
                hide_in_project=hide_in_project,
            )

    @strawberry.field(description="All the ambientes belonging to this obra.")
    def ambientes(self, info: ResourceInfo) -> typing.List["Ambiente"]:
        ambientes_data = info.context["resource_manager"].database_manager.query(
            """
        SELECT ambiente.id, ambiente.nombre, ambiente.descripcion, ambiente.indice FROM ambiente
        JOIN obra ON ambiente.obra_id = obra.id
        WHERE obra.id = %s ORDER BY indice;
        """,
            (self.id,),
        )

        return [
            Ambiente(
                id=ambiente[0],
                name=ambiente[1],
                description=ambiente[2],
                index=ambiente[3],
            )
            for ambiente in ambientes_data
        ]


@strawberry.type(description="An ambiente is a section of an obra. It contains images.")
class Ambiente:
    id: int = strawberry.field(description="The ID of the ambiente in the database.")
    name: str = strawberry.field(description="The  name of the ambiente.")
    description: typing.Optional[str] = strawberry.field(
        description="The description of the ambiente in markdown format. Can be null."
    )
    index: float = strawberry.field(
        description="The index of the ambiente for UI ordering purposes. It's a float due to how the database handles reordering."
    )

    @strawberry.field(description="The obra this ambiente belongs to.")
    def obra(self, info: ResourceInfo) -> Obra:
        obra_data = info.context["resource_manager"].database_manager.query(
            """
        SELECT obra.id, obra.nombre, obra.descripcion, obra.area, obra.indice, publico FROM obra
        JOIN ambiente ON ambiente.obra_id = obra.id
        WHERE ambiente.id = %s;
        """,
            (self.id,),
            count=1,
        )

        return Obra(
            id=obra_data[0],
            name=obra_data[1],
            description=obra_data[2],
            area=obra_data[3],
            index=obra_data[4],
            public=obra_data[5],
        )

    @strawberry.field(description="The images of this ambiente.")
    def images(self, info: ResourceInfo) -> typing.List["Image"]:
        images_data = info.context["resource_manager"].database_manager.query(
            """
        SELECT imagen.id, imagen.archivo, imagen.texto_alt, imagen.indice, pagina_principal, imagen.descripcion, 
        imagen.descripcionTipografia, esconderEnObra FROM imagen
        JOIN ambiente ON imagen.ambiente_id = ambiente.id
        WHERE ambiente.id = %s ORDER BY indice;
        """,
            (self.id,),
        )

        return [
            Image(
                id=image[0],
                filename=image[1],
                alt_text=image[2],
                index=image[3],
                main_page=image[4],
                description=image[5],
                description_font=image[6],
                hide_in_project=image[7],
            )
            for image in images_data
        ]


@strawberry.type(description="An image along a description of it.")
class Image:
    id: int = strawberry.field(description="The ID of the image in the database.")
    filename: str = strawberry.field(
        description="The unique filename of the image. **Use this to fetch the actual image.**"
    )
    alt_text: str = strawberry.field(
        description="The alt text of the image. Not to be shown in the UI."
    )
    description: typing.Optional[str] = strawberry.field(
        description="The description of the image."
    )
    description_font: str = strawberry.field(
        description="The font of the description text."
    )
    index: float = strawberry.field(
        description="The index of the image for UI ordering purposes. It's a float due to how the database handles reordering."
    )
    main_page: bool = strawberry.field(
        description="Indicates if an image should be shown in the main page of the website."
    )
    hide_in_project: bool = strawberry.field(
        description="Indicates if the image should be hidden in the project page."
    )

    @strawberry.field(
        description="The configuration for this image when shown in a obra page in mobile."
    )
    def phone_config(self, info: ResourceInfo) -> "PhoneImageConfig":
        # Done with a function since images are returned from multiple different places
        # wit slightly different queries then a generic resolver doesn't work and
        # having to repeat this code everywhere isn't good.
        # This may cause some performance issues since it's a new query for every image
        # but this ain't a critical app ¯\_(ツ)_/¯.
        phone_config_data = info.context["resource_manager"].database_manager.query(
            """
            SELECT (tlfnConfig).* FROM imagen WHERE imagen.id = %s;
        """,
            (self.id,),
            count=1,
        )

        borders_data = int(phone_config_data[0], 2)

        borders = Borders(
            n=borders_data & 0b1000,
            s=borders_data & 0b0100,
            e=borders_data & 0b0010,
            o=borders_data & 0b0001,
        )
        return PhoneImageConfig(
            borders=borders,
            alignment=enums.Alignment[phone_config_data[1]],
            descriptionPos=(
                enums.Direction[phone_config_data[2]] if phone_config_data[2] else None
            ),
            descriptionAlignment=phone_config_data[3],
        )

    @strawberry.field(description="The ambiente this image belongs to.")
    def ambiente(self, info: ResourceInfo) -> Ambiente:
        ambiente_data = info.context["resource_manager"].database_manager.query(
            """
        SELECT ambiente.id, ambiente.nombre, ambiente.descripcion, ambiente.indice FROM ambiente
        JOIN imagen ON imagen.ambiente_id = ambiente.id
        WHERE imagen.id = %s;
        """,
            (self.id,),
            count=1,
        )

        return Ambiente(
            id=ambiente_data[0],
            name=ambiente_data[1],
            description=ambiente_data[2],
            index=ambiente_data[3],
        )

    @strawberry.field(
        description="The configuration for the image if it's shown in the main page. Only exists if image.mainPage is true."
    )
    def mainImageConfig(self, info: ResourceInfo) -> typing.Optional["MainImageConfig"]:
        data = info.context["resource_manager"].database_manager.query(
            """
            SELECT imagenConfig.id, imagenConfig.descripcion, descripcion_en, logo_ubicacion, texto_ubicacion, sangrar,
            imagen_borde_n, imagen_borde_s, imagen_borde_e, imagen_borde_o,
            logo_borde_n, logo_borde_s, logo_borde_e, logo_borde_o,
            descripcionTamano, imagenConfig.descripcionDistribucion, imagenConfig.descripcionTipografia
            FROM imagenConfig JOIN imagen on imagenConfig.imagen_id = imagen.id 
            WHERE imagen.id = %s AND imagen.pagina_principal;
            """,
            (self.id,),
            1,
        )

        if data:
            return MainImageConfig(
                id=data[0],
                description=data[1],
                description_en=data[2],
                logo_pos=data[3],
                description_pos=data[4],
                overflow=data[5],
                image_borders=Borders(n=data[6], s=data[7], e=data[8], o=data[9]),
                logo_borders=Borders(n=data[10], s=data[11], e=data[12], o=data[13]),
                description_font_size=data[14],
                description_alignment=data[15],
                description_font=data[16],
            )


@strawberry.type(
    description="The configuration for an image when shown in a specific obra page in mobile."
)
class PhoneImageConfig:
    borders: "Borders" = strawberry.field(
        description="Indicates what borders the image should have."
    )
    alignment: enums.Alignment = strawberry.field(
        description="The alignment of the image."
    )
    descriptionPos: typing.Optional[enums.Direction] = strawberry.field(
        description="The position of the description relative to the image."
    )
    descriptionAlignment: str = strawberry.field(
        description="The alignment of the description."
    )


@strawberry.type(
    description="The configuration for an image that it's shown in the main page."
)
class MainImageConfig:
    id: int = strawberry.field(
        description="The id of this image config in the database."
    )
    description: typing.Optional[str] = strawberry.field(
        description="The description of this image in Spanish."
    )
    description_en: typing.Optional[str] = strawberry.field(
        description="The description of this image in English."
    )
    description_pos: typing.Optional[enums.Direction] = strawberry.field(
        description="The position of the description relative to the image. Null means it shouldn't be shown."
    )
    description_alignment: str = strawberry.field(
        description="The alignment of the description text."
    )
    description_font: str = strawberry.field(
        description="The font of the description text."
    )
    description_font_size: float = strawberry.field(
        description="The font size of the description text in rem units."
    )
    logo_pos: typing.Optional[enums.Direction] = strawberry.field(
        description="The position of the logo relative to the image. Null means it shouldn't be shown."
    )
    logo_borders: "Borders"
    image_borders: "Borders"
    overflow: bool = strawberry.field(
        description="Indicates if the image should reach the border of the screen."
    )

    @strawberry.field(description="The image that owns this configuration.")
    def image(self, info: ResourceInfo) -> Image:
        data = info.context["resource_manager"].database_manager.query(
            """
            SELECT id, archivo, textoAlt, indice, imagen_principal, descripcion, descripcionTipografia, esconderEnObra FROM imagen 
            JOIN imagenConfig ON imagenConfig.imagen_id = imagen.id
            WHERE imagenConfig.id = %s;
        """,
            (self.id,),
            1,
        )

        return Image(
            id=data[0],
            filename=data[1],
            alt_text=data[2],
            index=data[3],
            main_page=data[4],
            description=data[5],
            description_font=data[6],
            hide_in_project=data[7],
        )


@strawberry.type(
    description="The result of an obra query. It contains the page and page count of the result."
)
class ObraResult:
    page: int = strawberry.field(description="The current page of the result.")
    page_count: int = strawberry.field(
        description="The amount of pages that can be queried for results."
    )
    obras: typing.List[Obra] = strawberry.field(
        description="All the obras returned by the current page."
    )


@strawberry.type(
    description="The result of an ambiente query. It contains the page and page count of the result."
)
class AmbienteResult:
    page: int = strawberry.field(description="The current page of the result.")
    page_count: int = strawberry.field(
        description="The amount of pages that can be queried for results."
    )
    ambientes: typing.List[Ambiente] = strawberry.field(
        description="All the ambientes returned by the current page."
    )


@strawberry.type(
    description="The result of an images query. It contains the page and page count of the result."
)
class ImageResult:
    page: int = strawberry.field(description="The current page of the result.")
    page_count: int = strawberry.field(
        description="The amount of pages that can be queried for results."
    )
    images: typing.List[Image] = strawberry.field(
        description="All the images returned by the current page."
    )


@strawberry.type(description="Determines what borders a resource should have.")
class Borders:
    n: bool = strawberry.field(
        description="Determines if the resource should have a border on the top."
    )
    s: bool = strawberry.field(
        description="Determines if the resource should have a border on the bottom."
    )
    e: bool = strawberry.field(
        description="Determines if the resource should have a border on left."
    )
    o: bool = strawberry.field(
        description="Determines if the resource should have a border on right."
    )
