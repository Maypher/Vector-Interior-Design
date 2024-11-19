from flask import Flask
from os import environ
from routes import obra_routes

app = Flask(__name__)
app.secret_key = environ.get("SECRET_KEY")
app.register_blueprint(obra_routes)

"""
The database and obras files are copied from the admin backend since they both have the exact same functionality.
Not the best I know but it is what it is ＜（＾－＾）＞
"""


@app.route("/")
def test():
    return "Hello"


if __name__ == "__main__":
    app.run(port=environ.get("PORT"), host="0.0.0.0", debug=True)
