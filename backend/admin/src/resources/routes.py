from flask import Blueprint, request, jsonify
import resources.obra as obra
from auth.authentication import login_required

obra_routes = Blueprint("resource_creation", __name__, url_prefix="/obras")


@obra_routes.get("/")
def get_obras():
    try:
        page = request.args.get("pagina", 1)
        # This is done because if page is an empty parameter
        # it gets saved as "" not causing the raise and getting
        # passed to the function as is.
        if page:
            page = int(page)
        else:
            raise ValueError
    except ValueError:
        return "Invalid page number.", 400

    obras = obra.get_obras(page)

    return jsonify(obras)


@obra_routes.get("/<int:id>")
def get_obra(id: int):
    found_obra = obra.get_obra_by_id(id)

    return (jsonify(found_obra), 200) if found_obra else ("", 404)


@obra_routes.post("/crear")
@login_required
def new_work():
    nombre = request.form.get("name")
    description = request.form.get("description")
    images = request.files.getlist("image")
    alt_texts = request.form.getlist("alt_text")

    if not nombre or not description:
        return "Name and description required.", 400

    if len(images) != len(alt_texts):
        return "Image count doesn't match alt texts", 400

    work_id = obra.new_obra(nombre, description, images, alt_texts)

    return (
        jsonify({"msg": f"Work {nombre} created successfully.", "work_id": work_id}),
        200,
    )


@obra_routes.delete("/borrar/<int:id>")
@login_required
def delete_obra(id: int):
    obra_exists = obra.get_obra_by_id(id)
    if obra_exists:
        obra.delete_obra(id)
        return f"Obra {obra_exists.name} (ID: {id}) deleted successfully.", 200
    return f"Obra with ID {id} doesn't exist", 404
