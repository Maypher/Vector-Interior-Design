from flask import Blueprint, request
from admin.resources import obra
from auth import login_required
from psycopg import errors

ambiente_admin_routes = Blueprint("ambiente", __name__, url_prefix="/ambientes")


@ambiente_admin_routes.post("/crear")
@login_required
def new_ambiente():
    form = request.form

    obra_id = form.get("obra_id")
    name = form.get("name")
    description = form.get("description")

    if not name:
        return "Nuevo ambiente requiere un nombre.", 400

    ambiente_id = None

    try:
        ambiente_id = obra.create_ambiente(obra_id, name, description)
    except errors.UniqueViolation as e:
        err_name = e.diag.constraint_name

        if err_name == "repeated_name":
            return "Un ambiente con este nombre ya existe para esta obra.", 409
        elif err_name == "repeated_index_ambiente":
            return "Un ambiente no puede repetir indice.", 409
    except errors.ForeignKeyViolation:
        return f"La obra con ID {obra_id} no existe.", 409

    return str(ambiente_id), 200


@ambiente_admin_routes.delete("/borrar/<int:id>")
@login_required
def delete_ambiente_by_id(id: int):
    ambiente = obra.get_ambiente_by_id(id)

    if ambiente:
        obra.delete_ambiente(id)
        return f"Ambiente '{ambiente.name}' (ID: {id}) borrado con éxito.", 200
    return f"Ambiente con ID {id} no existe.", 404


@ambiente_admin_routes.put("/actualizar/<int:id>")
@login_required
def update_ambiente(id: int):
    name = request.form.get("name")
    description = request.form.get("description")
    index = request.form.get("index")

    try:
        index = int(index)
    except TypeError:
        index = None

    ambiente = obra.get_ambiente_by_id(id)

    if not ambiente:
        return f"Ambiente con ID {id} no encontrado.", 404

    try:
        obra.update_ambiente(ambiente.id, name, description, index)
    except errors.UniqueViolation as e:
        err_name = e.diag.constraint_name

        if err_name == "repeated_name":
            return "Un ambiente con este nombre ya existe para esta obra.", 409
        elif err_name == "repeated_index_ambiente":
            return "Un ambiente no puede repetir indice.", 409
    except errors.ForeignKeyViolation:
        return f"El ambiente con el ID {ambiente.id} no existe.", 409

    return "", 200
