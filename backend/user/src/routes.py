from flask import Blueprint, request, jsonify
import obra

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

    name = request.args.get("nombre")

    if name:
        obras = obra.get_obras_by_name(name, page)
    else:
        obras = obra.get_obras(page)

    return jsonify(obras)


@obra_routes.get("/<int:id>")
def get_obra(id: int):
    found_obra = obra.get_obra_by_id(id)

    return (jsonify(found_obra), 200) if found_obra else ("", 404)
