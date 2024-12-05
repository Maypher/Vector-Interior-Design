from flask import Flask, request, jsonify
from os import environ, getenv
from common import obra

app = Flask(__name__)
app.secret_key = environ.get("SECRET_KEY")


@app.get("/")
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
        obras = obra.get_obras_by_name(name, page)
    else:
        obras = obra.get_obras(page)

    return jsonify(obras)


@app.get("/<int:id>")
def get_obra(id: int):
    found_obra = obra.get_obra_by_id(id)

    return (jsonify(found_obra), 200) if found_obra else ("", 404)


if __name__ == "__main__":
    app.run(port=environ.get("PORT"), host="0.0.0.0", debug=True)
