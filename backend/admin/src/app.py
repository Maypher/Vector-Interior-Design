from flask import Flask, jsonify
from os import environ
from db.migrations import apply_migrations
from auth.routes import auth_blueprint
from resources.routes import obra_routes

app = Flask(__name__)
app.secret_key = environ.get("SECRET_KEY")

app.register_blueprint(auth_blueprint)
app.register_blueprint(obra_routes)


@app.route("/")
def hello_world():
    return jsonify({"msg": "Hello"})


if __name__ == "__main__":
    apply_migrations()
    app.run(port=environ.get("PORT"), host="0.0.0.0", debug=True)
