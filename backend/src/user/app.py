from flask import Flask
from os import environ
from strawberry.flask.views import GraphQLView
from strawberry import Schema
from user.user_graphql import Query
from flask_cors import CORS
from flask import request

app = Flask(__name__)
app.secret_key = environ.get("SECRET_KEY")
CORS(app, origins="*")


app.add_url_rule(
    "/graphql",
    view_func=GraphQLView.as_view("graphql_user", schema=Schema(query=Query)),
)


@app.get("/")
def test():
    print(request.headers)

    return ""


if __name__ == "__main__":
    app.run(port=environ.get("PORT"), host="0.0.0.0", debug=True)
