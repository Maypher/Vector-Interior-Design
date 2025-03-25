import typing
import strawberry
from common.common_graphql import enums
from common.types import ResourceInfo
from psycopg import rows
from os import environ
from common.utilities.environment import dev_mode
from common.utilities.cdn import gen_image_url
from sanic.log import logger


@strawberry.type(description="The main structure of the database.")
class Project:
    id: int = strawberry.field(description="The ID of the project in the database.")
    name: str = strawberry.field(description="The name of the project.")
    description_es: str = (
        strawberry.field(
            description="The description of the project in Spanish written in markdown format."
        ),
    )
    description_en: str = strawberry.field(
        description="The description of the project in English in markdown syntax."
    )
    area: int = strawberry.field(
        description="The area of the project in meters squared."
    )
    index: float = strawberry.field(
        description="The index of the project for UI ordering purposes. It's a float due to how the database handles reordering."
    )
    public: bool = strawberry.field(
        description="Indicates if the project is available in the public end of the website."
    )
    main_image: strawberry.Private[
        int
    ]  # The id of the thumbnail private because in it of itself it's not exposed. Only used to retrieve the thumbnail

    @strawberry.field(
        description="A project can have a thumbnail that will be the first thing shown in the UI."
    )
    def thumbnail(self, info: ResourceInfo) -> typing.Optional["Image"]:
        return info.context["resource_manager"].database_manager.query(
            """
            SELECT * FROM image 
            WHERE id = %s;
        """,
            (self.main_image,),
            count=1,
            row_factory=rows.class_row(Image),
        )

    @strawberry.field(description="All the spaces belonging to this project.")
    def spaces(self, info: ResourceInfo) -> typing.List["Space"]:
        return info.context["resource_manager"].get_spaces_by_project(self.id)


@strawberry.type(description="A space is a section of a project. It contains images.")
class Space:
    id: int = strawberry.field(description="The ID of the space in the database.")
    name: str = strawberry.field(description="The  name of the space.")
    description_es: typing.Optional[str] = strawberry.field(
        description="The description of the space in Spanish in markdown format. Can be null."
    )
    description_en: typing.Optional[str] = strawberry.field(
        description="The description of the space in English in markdown format. Can be null."
    )
    index: float = strawberry.field(
        description="The index of the space for UI ordering purposes. It's a float due to how the database handles reordering."
    )
    project_id: strawberry.Private[int]  # The id of the project this space belongs to

    @strawberry.field(description="The project this space belongs to.")
    def project(self, info: ResourceInfo) -> Project:
        project_data = info.context["resource_manager"].database_manager.query(
            """
        SELECT * FROM project
        WHERE id=%s;
        """,
            (self.project_id,),
            count=1,
        )

        return Project(**project_data)

    @strawberry.field(description="The images of this ambiente.")
    def images(
        self, info: ResourceInfo, show_hidden: bool = False
    ) -> typing.List["Image"]:
        image_data = info.context["resource_manager"].database_manager.query(
            f"""
        SELECT image.* FROM image
        JOIN space ON image.space_id = space.id
        WHERE space.id = %s {"AND NOT image.hide_in_project" if show_hidden else ""} ORDER BY index;
        """,
            (self.id,),
        )

        return [Image(**image) for image in image_data]


@strawberry.type(description="An image along a description of it.")
class Image:
    base_url: str = environ.get("IMAGES_URL")
    id: int = strawberry.field(description="The ID of the image in the database.")
    filename: str = strawberry.field(
        description="The filename of the image in the database. Don't use this for showing the image in the frontend. Instead use `imageUrl`."
    )
    alt_text_es: str = strawberry.field(
        description="The alt text of the image in Spanish. Not to be shown in the UI."
    )
    alt_text_en: str = strawberry.field(
        description="The alt text of the image in English. Not to be shown in the UI."
    )
    description_es: typing.Optional[str] = strawberry.field(
        description="The description of the image in Spanish."
    )
    description_en: typing.Optional[str] = strawberry.field(
        description="The description of the image in English."
    )
    description_font: str = strawberry.field(
        description="The font of the description text."
    )
    sculpture: bool = (
        strawberry.field(description="Indicates that this image is an sculpture"),
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
    bg_color: str = strawberry.field(
        description="The color of the background for this image in hexadecimal format #rrggbb (# included)"
    )
    space_id: strawberry.Private[int]  # The id of the space this image belongs to.
    # Since the db returns this as a tuple string '(borders, alignment, description_pos, description_alignment)'
    # This needs to be preprocessed before being sent. That's why there are two phone_config fields
    phone_config: strawberry.Private[str]
    desktop_config: strawberry.Private[str]

    @strawberry.field(
        description="The configuration for this image when shown in a project page in mobile."
    )
    def phoneConfig(self) -> "PhoneImageConfig":
        return PhoneImageConfig.from_db(self.phone_config)

    @strawberry.field(
        description="The configuration for this image when shown in a project page in desktop."
    )
    def desktopConfig(self) -> "DesktopImageConfig":
        return DesktopImageConfig.from_db(self.desktop_config)

    @strawberry.field(description="The space this image belongs to.")
    def space(self, info: ResourceInfo) -> Space:
        return info.context["resource_manager"].database_manager.query(
            """
        SELECT * FROM space
        WHERE id = %s;
        """,
            (self.space_id,),
            count=1,
            row_factory=rows.class_row(Space),
        )

    @strawberry.field(
        description="The configuration for the image if it's shown in the main page. Only exists if image.mainPage is true."
    )
    def mainImageConfig(
        self, info: ResourceInfo
    ) -> typing.Optional["MainPageImageConfig"]:
        main_page_config = info.context["resource_manager"].database_manager.query(
            """
            SELECT main_page_config.* FROM main_page_config JOIN image on main_page_config.image_id = image.id 
            WHERE image.id = %s AND image.main_page;
            """,
            (self.id,),
            1,
        )

        return MainPageImageConfig(**main_page_config)

    @strawberry.field(description="The data for this image if it's a sculpture.")
    def sculpture_data(self, info: ResourceInfo) -> typing.Optional["SculptureData"]:
        return info.context["resource_manager"].database_manager.query(
            """
            SELECT sculpture_data.* FROM sculpture_data JOIN image on sculpture_data.image_id = image.id 
            WHERE image.id = %s AND image.sculpture;
            """,
            (self.id,),
            1,
            row_factory=rows.class_row(SculptureData),
        )

    @strawberry.field(description="The url used to fetch the image in the frontend")
    def image_url(self, info: ResourceInfo) -> str:
        return f"{environ.get("IMAGES_URL")}{self.filename}"


@strawberry.type(
    description="The configuration for an image when shown in a specific project's page in mobile."
)
class PhoneImageConfig:
    borders: "Borders" = strawberry.field(
        description="Indicates what borders the image should have."
    )
    alignment: enums.Alignment = strawberry.field(
        description="The alignment of the image."
    )
    descriptionPos: typing.Optional[enums.Location] = strawberry.field(
        description="The position of the description relative to the image."
    )
    descriptionAlignment: str = strawberry.field(
        description="The alignment of the description."
    )

    @staticmethod
    def from_db(data: str) -> "PhoneImageConfig":
        # Since the data is returned from the db as a string in the form (borders, alignment, description_pos, description_alignment)
        #  it needs to be transformed into a tuple.
        # Doing data[1:-1] since the string is surrounded by parentheses.
        data = tuple(data[1:-1].split(","))

        borders_data = int(data[0], 2)

        return PhoneImageConfig(
            borders=Borders.from_bits(borders_data),
            alignment=enums.Alignment[data[1]],
            descriptionPos=(enums.Location[data[2]] if data[2] else None),
            descriptionAlignment=data[3],
        )


@strawberry.type(
    description="The configuration for an image when shown in a specific project's page in desktop."
)
class DesktopImageConfig:
    group_alignment: typing.Optional[enums.ImageGroupAlignment]
    group_end: bool
    image_size: int
    image_borders: "Borders"
    description_position: typing.Optional[enums.Location]
    description_alignment: str
    description_borders: "Borders"
    description_logo_position: typing.Optional[enums.Location]
    logo_position: typing.Optional[enums.Location]
    logo_borders: "Borders"

    @staticmethod
    def from_db(data: str) -> "DesktopImageConfig":
        # Since the data is returned from the db as a string in the form
        # (group_alignment, group_end, image_size, image_borders, description_position, description_alignment, description_borders, description_logo_position, logo_position, logo_borders)
        #  it needs to be transformed into a tuple.
        # Doing data[1:-1] since the string is surrounded by parentheses.
        data = tuple(data[1:-1].split(","))

        image_borders = int(data[3], 2)
        description_borders = int(data[6], 2)
        logo_borders = int(data[9], 2)

        return DesktopImageConfig(
            group_alignment=data[0] or None,
            group_end=data[1] == "t",
            image_size=data[2],
            image_borders=Borders.from_bits(image_borders),
            description_position=enums.Location[data[4]] if data[4] else None,
            description_alignment=data[5],
            description_borders=Borders.from_bits(description_borders),
            description_logo_position=enums.Location[data[7]] if data[7] else None,
            logo_position=enums.Location[data[8]] if data[8] else None,
            logo_borders=Borders.from_bits(logo_borders),
        )


@strawberry.type(
    description="The configuration for an image that it's shown in the main page."
)
class MainPageImageConfig:
    id: int = strawberry.field(
        description="The id of this image config in the database."
    )
    description_es: typing.Optional[str] = strawberry.field(
        description="The description of this image in Spanish."
    )
    description_en: typing.Optional[str] = strawberry.field(
        description="The description of this image in English."
    )
    description_font: str = strawberry.field(
        description="The font of the description text."
    )
    description_font_size: float = strawberry.field(
        description="The font size of the description text in rem units."
    )
    description_alignment: str = strawberry.field(
        description="The alignment of the description. Will be one of tailwind's text-align values."
    )
    bg_color: str = strawberry.field(
        description="The color of the background for this image in hexadecimal format #rrggbb (# included)"
    )
    image_size: int = strawberry.field(
        description="The relative size of the image in the main page. Goes from 0% to 100%."
    )
    index: float = strawberry.field(
        description="The index of this image in the main page in the form of a float."
    )
    phone_config: strawberry.Private[
        str
    ]  # Since it's returned from the db as a tuple string it needs preprocessing before being returned
    desktop_config: strawberry.Private[str]
    image_id: strawberry.Private[int]  # The id of the image this config belongs to.

    @strawberry.field(
        description="The configuration used to display on mobile devices."
    )
    def phoneConfig(self) -> "MainPageImagePhoneConfig":
        return MainPageImagePhoneConfig.from_db(self.phone_config)

    @strawberry.field(
        description="The configuration used to display on desktop devices."
    )
    def desktopConfig(self) -> "MainPageImageDesktopConfig":
        return MainPageImageDesktopConfig.from_db(self.desktop_config)

    @strawberry.field(description="The image that owns this configuration.")
    def image(self, info: ResourceInfo) -> Image:
        return info.context["resource_manager"].database_manager.query(
            """
            SELECT image.* FROM image
            JOIN main_page_config ON main_page_config.image_id = image.id
            WHERE main_page_config.id = %s;
        """,
            (self.id,),
            1,
            row_factory=rows.class_row(Image),
        )


@strawberry.type(
    description="The configuration of how an image will look on the main page of mobile."
)
class MainPageImagePhoneConfig:
    image_borders: "Borders"
    description_position: typing.Optional[enums.Location]
    logo_position: typing.Optional[enums.Location]
    logo_borders: "Borders"
    overflow: bool

    @staticmethod
    def from_db(data: str) -> "MainPageImagePhoneConfig":
        # Since the data is returned from the db as a string in the form
        # (image_borders, description_pos, logo_pos, logo_borders, overflow)
        # it needs to be transformed into a tuple.
        # Doing data[1:-1] since the string is surrounded by parentheses.
        data = tuple(data[1:-1].split(","))
        image_borders = int(data[0], 2)
        logo_borders = int(data[3], 2)

        return MainPageImagePhoneConfig(
            image_borders=Borders.from_bits(image_borders),
            description_position=data[1] or None,
            logo_position=data[2] or None,
            logo_borders=Borders.from_bits(logo_borders),
            overflow=data[4] == "t",
        )


@strawberry.type(
    description="The configuration of how an image will look on the main page of desktop."
)
class MainPageImageDesktopConfig:
    image_position: enums.DesktopImagePosition = strawberry.field(
        description="The position of the image in the screen."
    )
    description_position: typing.Optional[enums.Location] = strawberry.field(
        description="The position of the description relative to the image."
    )
    description_borders: "Borders" = strawberry.field(
        description="The borders of the description."
    )
    logo_position: typing.Optional[enums.Location] = strawberry.field(
        description="The position of the logo relative to the image."
    )
    logo_borders: "Borders" = strawberry.field(description="The borders of the logo")
    description_logo_position: typing.Optional[enums.Location] = strawberry.field(
        description="The position of the logo relative to the description."
    )
    description_logo_borders: "Borders" = strawberry.field(
        description="The borders of the description logo."
    )
    overflow: bool = strawberry.field(
        description="Determines if the image should overflow to the borders of the screen."
    )

    @staticmethod
    def from_db(data: str) -> "MainPageImageDesktopConfig":
        # Since the data is returned from the db as a string in the form
        # (image_position, description_pos, description_borders, logo_pos, logo_borders, description_logo_pos, description_logo_borders, overflow)
        # it needs to be transformed into a tuple.
        # Doing data[1:-1] since the string is surrounded by parentheses.
        data = tuple(data[1:-1].split(","))

        description_borders = int(data[2], 2)
        logo_borders = int(data[4], 2)
        description_logo_borders = int(data[6], 2)

        return MainPageImageDesktopConfig(
            image_position=data[0] or None,
            description_position=data[1] or None,
            description_borders=Borders.from_bits(description_borders),
            logo_position=data[3] or None,
            logo_borders=Borders.from_bits(logo_borders),
            description_logo_position=data[5] or None,
            description_logo_borders=Borders.from_bits(description_logo_borders),
            overflow=data[7] == "t",
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
    w: bool = strawberry.field(
        description="Determines if the resource should have a border on right."
    )

    @staticmethod
    def from_bits(bits: int) -> "Borders":
        """
        In the database borders are stored as a 4 bit value indicating (n, s, e, w) respectively.
        This method transforms it into its correct representation.
        """

        return Borders(
            n=bits & 0b1000,
            s=bits & 0b0100,
            e=bits & 0b0010,
            w=bits & 0b0001,
        )


@strawberry.type(description="The data for an image that represents a sculpture.")
class SculptureData:
    id: int = strawberry.field(description="The id of the data in the database.")
    image_id: strawberry.Private[int]  # The id of the image this data belongs to
    description_es: typing.Optional[str] = strawberry.field(
        description="The description of the sculpture in Spanish."
    )
    description_en: typing.Optional[str] = strawberry.field(
        description="The description of the sculpture in English."
    )
    bg_color: str = strawberry.field(
        description="The color of the background for this image in hexadecimal format #rrggbb (# included)"
    )
    index: float = strawberry.field(
        description="The float index of the sculpture relative to all others."
    )

    @strawberry.field(description="The image this data belongs to.")
    def image(self):
        return

    @strawberry.field(description="The image that owns this configuration.")
    def image(self, info: ResourceInfo) -> Image:
        return info.context["resource_manager"].database_manager.query(
            """
            SELECT image.* FROM image
            JOIN sculpture_data ON sculpture_data.image_id = image.id
            WHERE sculpture_data.id = %s;
        """,
            (self.id,),
            1,
            row_factory=rows.class_row(Image),
        )
