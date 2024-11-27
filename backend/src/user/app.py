from flask import Flask
from os import environ
from common.routes import obra_fetch_routes

app = Flask(__name__)
app.secret_key = environ.get("SECRET_KEY")
app.register_blueprint(obra_fetch_routes)


@app.route("/")
def test():
    return "Hello"


if __name__ == "__main__":
    app.run(port=environ.get("PORT"), host="0.0.0.0", debug=True)
