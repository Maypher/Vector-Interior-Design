import typing
import strawberry
from common.database import generic_database
from common.common_graphql.enums import Direction


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
    def thumbnail(self) -> typing.Optional["Image"]:
        image_data = generic_database.query(
            """
            SELECT imagen.id, archivo, texto_alt, imagen.indice, pagina_principal FROM imagen 
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

            return Image(
                id=image_id,
                filename=filename,
                alt_text=alt_text,
                index=image_index,
                main_page=main_page,
            )

    @strawberry.field(description="All the ambientes belonging to this obra.")
    def ambientes(self) -> typing.List["Ambiente"]:
        ambientes_data = generic_database.query(
            """
        SELECT ambiente.id, ambiente.nombre, ambiente.descripcion, ambiente.indice FROM ambiente
        JOIN obra ON ambiente.obra_id = obra.id
        WHERE obra.id = %s;
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
    def obra(self) -> Obra:
        obra_data = generic_database.query(
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
    def images(self) -> typing.List["Image"]:
        images_data = generic_database.query(
            """
        SELECT imagen.id, imagen.archivo, imagen.texto_alt, imagen.indice, pagina_principal FROM imagen
        JOIN ambiente ON imagen.ambiente_id = ambiente.id
        WHERE ambiente.id = %s;
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
    index: float = strawberry.field(
        description="The index of the image for UI ordering purposes. It's a float due to how the database handles reordering."
    )
    main_page: bool = strawberry.field(
        description="Indicates if an image should be shown in the main page of the website."
    )

    @strawberry.field(description="The ambiente this image belongs to.")
    def ambiente(self) -> Ambiente:
        ambiente_data = generic_database.query(
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
    def mainImageConfig(self) -> typing.Optional["MainImageConfig"]:
        data = generic_database.query(
            """
            SELECT imagenConfig.id, imagenConfig.descripcion, descripcion_en, logo_ubicacion, texto_ubicacion, sangrar 
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
    description_pos: typing.Optional[Direction] = strawberry.field(
        description="The position of the description relative to the image. Null means it shouldn't be shown."
    )
    logo_pos: typing.Optional[Direction] = strawberry.field(
        description="The position of the logo relative to the image. Null means it shouldn't be shown."
    )
    overflow: bool = strawberry.field(
        description="Indicates if the image should reach the border of the screen."
    )

    @strawberry.field(description="The image that owns this configuration.")
    def image(self) -> Image:
        data = generic_database.query(
            """
            SELECT * FROM imagen 
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
