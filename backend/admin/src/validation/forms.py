from marshmallow import (
    Schema,
    fields,
    validate,
    validates_schema,
    ValidationError,
    EXCLUDE,
)
from werkzeug.datastructures import FileStorage


class ImageInfo(Schema):
    filename = fields.String(
        required=True
    )  # Image to change. Doesn't actually change the name
    alt_text = fields.String(allow_none=True)
    index = fields.Int(validate=validate.Range(min=0), allow_none=True)


class CreateObraForm(Schema):
    class Meta:
        unknown = EXCLUDE

    name = fields.String(
        required=True, error_messages={"required": "Nombre de la obra es requerido."}
    )
    description = fields.String(
        required=True,
        error_messages={"required": "Descripción de la obra es requerida."},
    )
    images = fields.List(
        fields.Raw(),
        required=True,
        validate=validate.Length(
            min=1, error="La obra debe tener al menos una imagen."
        ),
    )
    alt_texts = fields.List(fields.Nested(ImageInfo))

    @validates_schema
    def validate_images(self, data: dict, **kwargs):
        images: list[FileStorage] = data.get("images", [])
        alt_texts: list[str] = data.get("alt_texts", [])

        errors = {}

        if not images:
            errors["images"] = ["La obra debe tener al menos una imagen."]

        if len(images) != len(alt_texts):
            err = ["Cantidad de imágenes y textos alternativos no coinciden."]
            errors["alt_texts"] = err
            errors["images"] = err

        for image in images:
            if image.mimetype not in ("image/png", "image/jpeg"):
                errors["images"] = [f"Imagen {image.filename} no es un archivo válido."]

        images_names = [image.filename for image in images]
        for alt_text in alt_texts:
            if alt_text.get("filename") not in images_names:
                err = f"Texto alternativo '{alt_text["alt_text"]}' no pertenece a ninguna imagen."
                if errors.get("alt_texts"):
                    errors["alt_texts"].append(err)
                else:
                    errors["alt_texts"] = [err]

        if errors:
            raise ValidationError(errors)


class UpdateObraForm(Schema):
    obra_id = fields.Int(required=True, validate=validate.Range(min=1))
    name = fields.String(allow_none=True)
    description = fields.String(allow_none=True)
    images_change = fields.List(fields.Nested(ImageInfo), allow_none=True)
    images_delete = fields.List(fields.String(), allow_none=True)
    images_new = fields.List(fields.Raw(), allow_none=True)
    images_new_info = fields.List(fields.Nested(ImageInfo), allow_none=True)

    @validates_schema
    def validate_images(self, data: dict, **kwargs):
        images_new: list[FileStorage] = data.get("images_new", [])
        images_new_info: list[dict[str, str]] = data.get("images_new_info", [])

        errors = {}

        if images_new and images_new_info:
            if len(images_new) != len(images_new_info):
                err = ["No hay suficiente información para añadir las imágenes."]
                errors["images_new"] = err
                errors["images_new_info"] = err
            for image_info in images_new_info:
                if not image_info.get("alt_text"):
                    err = f"Imagen '{image_info["filename"]}' requiere un texto alternativo."
                    if errors.get("images_new_info"):
                        errors["images_new_info"].append(err)
                    else:
                        errors["images_new_info"] = [err]
        elif images_new and not images_new_info:
            errors["images_new"] = ["Imágenes requieren texto alternativo."]
        elif images_new_info and not images_new:
            errors["images_new_info"] = [
                "Texto alternativo encontrado sin ninguna imagen."
            ]

        if errors:
            raise ValidationError(errors)


class DeleteObraForm(Schema):
    id = fields.Int(
        validate=validate.Range(
            min=1,
            error="El ID de la obra a borrar debe ser mayor a 0. Recibió '{input}'.",
        ),
        required=True,
        error_messages={"required": "Se requiere un ID para borrar una obra."},
    )
