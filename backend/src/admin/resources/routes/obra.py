from flask import Blueprint, request, jsonify
from admin.resources import obra
from auth import login_required
from psycopg import errors
from strawberry import Schema
from strawberry.flask.views import GraphQLView
from admin.resources.admin_graphql import AuthGraphQLView, Query, Mutation

obra_admin_routes = Blueprint("obra", __name__, url_prefix="/obras")

obra_admin_routes.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view(
        "graphql_view",
        schema=Schema(query=Query, mutation=Mutation),
        graphql_ide="graphiql",
        multipart_uploads_enabled=True,
    ),
)


@obra_admin_routes.get("/")
@login_required
def get_obras():
    try:
        page = request.args.get("page", 1)
        # This is done because if page is an empty parameter
        # it gets saved as "" not causing the raise and getting
        # passed to the function as is.
        if page:
            page = int(page)
            if page < 1:
                return "Página debe ser mayor a 0.", 400
        else:
            raise ValueError
    except ValueError:
        return "Número de página invalido.", 400

    try:
        page_size = request.args.get("page_size", 10)

        if page_size:
            page_size = int(page_size)
        else:
            raise ValueError
    except ValueError:
        return "Tamaño de página invalido.", 400

    name = request.args.get("name")

    if name:
        obras = obra.get_obras_by_name(name, page, page_size, True)
    else:
        obras = obra.get_obras(page, page_size, True)

    return jsonify(obras)


@obra_admin_routes.get("/<int:id>")
@login_required
def get_obra(id: int):
    found_obra = obra.get_obra_by_id(id, True)

    return (jsonify(found_obra), 200) if found_obra else ("", 404)


@obra_admin_routes.post("/crear")
@login_required
def new_obra():
    form = request.form

    name = form.get("name")
    description = form.get("description")
    area = form.get("area")

    if not name:
        return "Nueva obra requiere un nombre.", 400
    if not description:
        return "Nueva obra requiere una descripción.", 400
    if not area:
        return "Nueva obra requiere un área.", 400

    obra_id = obra.create_obra(name, description, area)

    return f"{obra_id}", 200


@obra_admin_routes.delete("/borrar/<int:id>")
@login_required
def delete_obra(id: int):
    obra_exists = obra.get_obra_by_id(id, True)

    if obra_exists:
        obra.delete_obra(id)
        return f"Ambiente {obra_exists.name} (ID: {id}) borrada exitosamente.", 200
    return f"Obra con ID {id} no existe.", 404


@obra_admin_routes.put("/actualizar/<int:id>")
@login_required
def update_obra(id: int):
    name = request.form.get("name")
    description = request.form.get("description")
    public = request.form.get("public")
    area = request.form.get("area")
    index = request.form.get("index")
    thumbnail = request.form.get("thumbnail")

    try:
        area = int(area)
    except TypeError:
        area = None

    try:
        index = int(index)
    except TypeError:
        index = None

    obra_model = obra.get_obra_by_id(id, True)

    if not obra_model:
        return f"Obra con ID {id} no encontrada.", 404

    if index and not index.isdecimal() and float(index) < 1:
        return f"Indice '{index}' debe ser un dígito mayor a 0."

    try:
        obra.update_obra(id, name, description, area, thumbnail, index, public)
    except errors.DatabaseError as e:
        if e.sqlstate == "P0001":
            return "Imagen debe pertenecer a esta obra para ser imagen principal."
        else:
            raise e
    return "", 200
