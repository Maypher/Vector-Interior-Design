from flask import Flask
from os import environ
from admin.auth.routes import auth_blueprint
from admin.resources import obra_admin_routes, image_admin_routes, ambiente_admin_routes
from flask_cors import CORS

from sanic import Sanic


def create_app() -> Sanic:
    app = Sanic("TQ-admin-backend")
    return app


app = Flask(__name__)
app.secret_key = environ.get("SECRET_KEY")
CORS(
    app,
    supports_credentials=True,
    origins=[environ.get("FRONTEND_URL"), "https://192.168.0.8:5173"],
)
app.config.update(
    SESSION_COOKIE_SAMESITE="None",
    SESSION_COOKIE_SECURE=True,  # Required for "None", set to False if not using HTTPS
)

app.register_blueprint(auth_blueprint)
app.register_blueprint(obra_admin_routes)
app.register_blueprint(ambiente_admin_routes)
app.register_blueprint(image_admin_routes)

if __name__ == "__main__":
    app = create_app()

    port = environ.get("PORT", 8080)

    try:
        port = int(port)
    except ValueError:
        print("Port must be an integer number.")
        exit(1)

    app.run(host="0.0.0.0", port=port)
