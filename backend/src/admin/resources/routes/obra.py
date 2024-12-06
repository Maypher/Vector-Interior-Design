from flask import Blueprint, request, jsonify
from admin.resources import obra
from auth import login_required
from psycopg import errors

obra_admin_routes = Blueprint("obra", __name__, url_prefix="/obras")


@obra_admin_routes.get("/")
def get_obras():
    try:
        page = request.args.get("page", 1)
        # This is done because if page is an empty parameter
        # it gets saved as "" not causing the raise and getting
        # passed to the function as is.
        if page:
            page = int(page)
        else:
            raise ValueError
    except ValueError:
        return "Número de página invalido.", 400

    name = request.args.get("name")

    if name:
        obras = obra.get_obras_by_name(name, page, allow_private=True)
    else:
        obras = obra.get_obras(page, allow_private=True)

    return jsonify(obras)


@obra_admin_routes.get("/<int:id>")
def get_obra(id: int):
    found_obra = obra.get_obra_by_id(id, True)

    return (jsonify(found_obra), 200) if found_obra else ("", 404)


@obra_admin_routes.post("/crear")
@login_required
def new_obra():
    form = request.form

    name = form.get("name")
    description = form.get("description")

    if not name:
        return "Nueva obra requiere un nombre.", 400
    if not description:
        return "Nueva obra requiere una descripción.", 400

    obra_id = obra.create_obra(name, description)

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
    thumbnail = request.form.get("thumbnail")

    obra_model = obra.get_obra_by_id(id, True)

    if not obra_model:
        return f"Obra con ID {id} no encontrada.", 404

    try:
        obra.update_obra(id, name, description, thumbnail, public)
    except errors.DatabaseError as e:
        if e.sqlstate == "P0001":
            return "Imagen debe pertenecer a esta obra para ser imagen principal."
    return "", 200
