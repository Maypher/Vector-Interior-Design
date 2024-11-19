from flask import Blueprint, request, jsonify
import resources.obra as obra
from auth.authentication import login_required

obra_routes = Blueprint("resource_creation", __name__, url_prefix="/obras")


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


@obra_routes.put("/actualizar/<int:id>")
def update_obra(id: int):
    obra_model = obra.get_obra_by_id(id)

    if not obra_model:
        return f"Obra with id {id} not found.", 404

    name = request.form.get("name")
    description = request.form.get("description")
    alt_text_images = request.form.getlist("alt_text_image")
    alt_text_change = request.form.getlist("alt_text_change")
    image_delete = request.form.getlist("image_delete")
    images_to_add = request.files.getlist("image_add")
    images_to_add_alt_text = request.form.getlist("image_add_alt_text")

    if len(alt_text_images) != len(alt_text_change):
        return (
            f"Amount of images to change alt text doesn't match amount of alt texts given.",
            400,
        )

    alt_text: list[obra.Image] = []

    for image_filename, new_alt_text in zip(alt_text_images, alt_text_change):
        # Get the image that should be updated
        image = obra.get_image(image_filename)

        if not image:
            return f"Can't update image {image_filename} alt text, not found", 404

        # Update its text (in memory) and query for update (in db)
        image.alt_text = new_alt_text
        alt_text.append(image)

    images_to_delete = []

    for filename in image_delete:
        image = obra.get_image(filename)

        if not image:
            return f"Can't delete {filename}, not found.", 404

        images_to_delete.append(image)

    if len(images_to_add) != len(images_to_add_alt_text):
        return (
            "Can't add new images. Amount of images to add doesn't match amount of alt texts",
            400,
        )

    new_images = list(zip(images_to_add, images_to_add_alt_text))

    obra.update_obra(
        id, name or None, description or None, images_to_delete, alt_text, new_images
    )
    return "", 200
