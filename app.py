import json

from flasgger import Swagger
from flask import Flask, jsonify, redirect
from werkzeug.exceptions import HTTPException

from config import Config
from mini_redis_api import RedisAPI


config = Config()

app = Flask(__name__)
swagger = Swagger(app)
app.register_blueprint(RedisAPI.blueprint, url_prefix="/mini-redis")


@app.errorhandler(HTTPException)
def handle_http_exception(e):
    """
    Handles HTTP exceptions
    """
    response = e.get_response()
    response.data = json.dumps(
        {
            "code": e.code,
            "name": e.name,
            "description": e.description,
        }
    )
    response.content_type = "application/json"
    return response


@app.errorhandler(Exception)
def handle_exception(e):
    """
    Handles non-HTTP exceptions
    """
    response = jsonify(
        {
            "code": 500,
            "name": "Internal Server Error",
            "description": str(e),
        }
    )
    response.status_code = 500
    return response


@app.route("/")
def redirect_to_apidocs():
    """
    Redirects all base requests to the API docs endpoint
    """
    return redirect("/apidocs")


if __name__ == "__main__":
    app.run(port=config.get_port(), debug=config.get_debug())
