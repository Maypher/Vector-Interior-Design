from flask import Blueprint, request, jsonify
from resources import obra
from auth import login_required
import json

from validation import forms
from marshmallow import ValidationError

obra_routes = Blueprint("resource_creation", __name__, url_prefix="/obras")


@obra_routes.post("/crear")
@login_required
def new_work():
    try:
        # Load it through the form to get better data structure and still be able to send files.
        # Not the best but it works.
        json_data = request.form.get("json")
        form = forms.CreateObraForm().load(
            {
                **json.loads(json_data),
                "images": request.files.getlist("images"),
            }
        )
    except ValidationError as e:
        return jsonify(e.messages), 400

    name = form.get("name")
    work_id = obra.new_obra(
        name, form.get("description"), form.get("images"), form.get("alt_texts")
    )

    return (
        jsonify({"msg": f"Work {name} created successfully.", "work_id": work_id}),
        200,
    )


@obra_routes.delete("/borrar/<int:id>")
@login_required
def delete_obra_by_id(id: int):
    try:
        forms.DeleteObraForm().load({"id": id})
    except ValidationError as e:
        return jsonify(e.messages), 400

    obra_exists = obra.get_obra_by_id(id)
    if obra_exists:
        obra.delete_obra(id)
        return f"Obra {obra_exists.name} (ID: {id}) deleted successfully.", 200
    return f"Obra with ID {id} doesn't exist", 404


@obra_routes.put("/actualizar/<int:id>")
@login_required
def update_obra(id: int):
    try:
        form = forms.UpdateObraForm().load(
            {
                **json.loads(request.form.get("json")),
                "obra_id": id,
                "images_new": request.files.getlist("images_new"),
            }
        )
    except ValidationError as e:
        return jsonify(e.messages), 400

    obra_model = obra.get_obra_by_id(id)

    if not obra_model:
        return f"Obra with id {id} not found.", 404

    obra.update_obra(
        id,
        form.get("name", None),
        form.get("description", None),
        form.get("images_delete", None),
        form.get("images_change", None),
        (
            list(zip(form.get("images_new"), form.get("images_new_info")))
            if form.get("images_new") and form.get("images_new_info")
            else None
        ),
    )
    return "", 200
