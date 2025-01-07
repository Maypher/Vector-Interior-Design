from common.database import DatabaseManager
from math import ceil
from common.common_graphql import schemas
import typing


class ResourceManager:
    database_manager: DatabaseManager
    allow_private: bool

    def __init__(self, database_manager: DatabaseManager):
        self.database_manager = database_manager
        self.allow_private = False

    def get_obra_by_id(self, id: int) -> typing.Optional[schemas.Obra]:
        """Returns the obra matching the given id or None."""
        data = self.database_manager.query(
            f"""
        SELECT obra.id, nombre, descripcion, publico, area, indice FROM obra
        WHERE obra.id = %s {"AND publico" if not self.allow_private else ""};
        """,
            (id,),
            1,
        )

        if not data:
            return None

        obra_id = int(data[0])
        name = data[1]
        description = data[2]
        publico = data[3]
        area = data[4]
        index = data[5]

        obra = schemas.Obra(
            id=obra_id,
            name=name,
            description=description,
            area=area,
            index=index,
            public=publico,
        )

        return obra

    def get_obras(self, page: int = 1, page_size: int = 10) -> schemas.ObraResult:
        """Retrieves a list of obras. Paginated by the given size"""
        offset = (page - 1) * page_size

        obra_ids = self.database_manager.query(
            f"""
            SELECT id FROM obra {"WHERE publico" if not self.allow_private else ""} 
            ORDER BY indice
            LIMIT %s OFFSET %s;
        """,
            (page_size, offset),
        )

        # I know this isn't the most efficient way but there will be at most 30 obras so ＜（＾－＾）＞.
        obras_count = self.database_manager.query(
            f"""
        SELECT COUNT(*) FROM obra {"WHERE publico" if not self.allow_private else ""};
        """,
            count=1,
        )[0]

        page_count = ceil(obras_count / page_size)

        return schemas.ObraResult(
            page=min(
                page, page_count
            ),  # Getting the min because if there are no obras then it would show up as 1/0
            page_count=page_count,
            obras=[
                obra
                for id in obra_ids
                if (obra := self.get_obra_by_id(id[0])) is not None
            ],
        )

    def get_obras_by_name(
        self, name: str, page: int = 1, page_size: int = 10
    ) -> schemas.AmbienteResult:
        """Returns all the obras like a given name. Paginated."""
        # Code repetition bad and single source of truth stfu.
        offset = (page - 1) * page_size
        obra_ids = self.database_manager.query(
            f"""
            SELECT id FROM obra
            WHERE obra.nombre ILIKE %s {"AND publico" if not self.allow_private else ""}
            ORDER BY indice
            LIMIT %s OFFSET %s;
        """,
            (f"%{name}%", page_size, offset),
        )

        obras_count = self.database_manager.query(
            f"""
        SELECT COUNT(*) FROM obra WHERE obra.nombre ILIKE %s {"AND publico" if not self.allow_private else ""};
        """,
            (f"%{name}%",),
            1,
        )[0]

        page_count = ceil(obras_count / page_size)

        return schemas.ObraResult(
            page=min(
                page, page_count
            ),  # Getting the min because if there are no obras then it would show up as 1/0
            page_count=page_count,
            obras=[
                obra
                for id in obra_ids
                if (obra := self.get_obra_by_id(id[0])) is not None
            ],
        )

    def get_ambiente_by_id(self, id: int) -> typing.Optional[schemas.Ambiente]:
        """Returns the ambiente matching the given id or None."""

        data = self.database_manager.query(
            f"""
        SELECT ambiente.id, ambiente.nombre, ambiente.descripcion, ambiente.indice
        FROM ambiente 
        {"JOIN obra ON ambiente.obra_id = obra.id" if not self.allow_private else ""}
        WHERE ambiente.id = %s {"AND obra.publico" if not self.allow_private else ""};
        """,
            (id,),
            1,
        )

        if not data:
            return None

        ambiente_id = data[0]
        nombre = data[1]
        description = data[2]
        index = data[3]

        return schemas.Ambiente(
            id=ambiente_id, name=nombre, description=description, index=index
        )

    def get_ambientes_by_obra(self, obra_id: int) -> list[schemas.Ambiente]:
        """Returns all ambientes for the given obra_id."""

        found_ambientes = self.database_manager.query(
            """
        SELECT ambiente.id 
        FROM obra INNER JOIN ambiente ON ambiente.obra_id = obra.id 
        WHERE obra.id = %s ORDER BY ambiente.indice;
        """,
            (obra_id,),
        )

        return [self.get_ambiente_by_id(int(id[0])) for id in found_ambientes]

    def get_image_by_filename(self, filename: str) -> typing.Optional[schemas.Image]:
        data = self.database_manager.query(
            f"""
            SELECT imagen.id, imagen.archivo, imagen.texto_alt, imagen.indice, imagen.pagina_principal, imagen.descripcion,
            imagen.descripcionTipografia, esconderEnObra FROM imagen 
            {"JOIN ambiente ON imagen.ambiente_id = ambiente.id JOIN obra ON ambiente.obra_id = obra.id" if not self.allow_private else ""}
            WHERE archivo = %s {"AND obra.publico" if not self.allow_private else ""};
            """,
            (filename,),
            count=1,
        )

        if data:
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
