from flask import Blueprint, request
from admin.resources import obra
from auth import login_required

image_admin_routes = Blueprint("images", __name__, url_prefix="/imagenes")


@image_admin_routes.post("/crear")
@login_required
def new_image():
    form = request.form

    alt_text = form.get("alt_text")
    ambiente_id = form.get("ambiente_id")

    amount_of_images = len(request.files)

    if amount_of_images == 0 or amount_of_images > 1:
        return "Solo se puede crear una imagen a la vez", 400

    image = request.files.get("image")

    if not alt_text:
        return "Nueva imagen requiere un texto alternativo.", 400
    if not ambiente_id:
        return "Nueva imagen debe estar relacionada a un ambiente.", 400

    filename = obra.create_image(image, alt_text, ambiente_id)

    # I know this isn't the best way but I don't want to create custom errors :)
    if not filename:
        return f"Ambiente con ID {ambiente_id} no existe o imagen inválida", 400

    return filename, 200


@image_admin_routes.delete("/borrar/<string:filename>")
@login_required
def delete_image(filename: str):

    obra.delete_image(filename)

    return f"imagen {filename} borrada con exitosamente.", 200


@image_admin_routes.put("/actualizar/<string:filename>")
@login_required
def update_image(filename: str):
    alt_text = request.form.get("alt_text")
    index = request.form.get("index")

    try:
        index = int(index)
    except TypeError:
        return f"Indice {index} es invalido.", 400

    if index < 0:
        return "Indice debe ser un número positivo", 400

    obra.update_image(filename, alt_text, index)
    return "", 200
