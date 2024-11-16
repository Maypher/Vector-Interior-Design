from flask import Flask, jsonify
from os import environ
from database.migrations import apply_migrations

app = Flask(__name__)


@app.route("/")
def hello_world():
    return jsonify({"msg": "Hello"})


if __name__ == "__main__":
    apply_migrations()
    app.run(port=environ.get("PORT"), host="0.0.0.0")
