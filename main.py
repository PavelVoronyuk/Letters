from flask import Flask, render_template
from flask_restx import Api
from letters.app import letters, ns_letters, page_not_found
from dotenv import load_dotenv
from os import getenv

load_dotenv()

app = Flask(__name__)
app.register_blueprint(letters, url_prefix="/letters")

app.config["SECRET_KEY"] = getenv("SECRET_KEY")

api = Api(app)
api.add_namespace(ns_letters)

app.register_error_handler(404, page_not_found)


if __name__ == "__main__":
    app.run(debug=True)