#!/usr/bin/python3
"""
Create a folder api at the root of the project 
                with an empty file __init__.py
Create a folder v1 inside api:
    create an empty file __init__.py
    create a file app.py:
        create a variable app, instance of Flask
        import storage from models
        import app_views from api.v1.views
        register the blueprint app_views to your
                                Flask instance app
        declare a method to handle @app.teardown_appcontext
                                that calls storage.close()
        inside if __name__ == "__main__":,
                run your Flask server (variable app) with:
            host = environment variable HBNB_API_HOST or 0.0.0.0
                                                    if not defined
            port = environment variable HBNB_API_PORT or 5000
                                                if not defined
            threaded=True
"""

#import os
#import sys

# Add the root directory to the Python path
#root_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..'))
#sys.path.insert(0, root_path)

from flask import Flask, jsonify, make_response
from models import storage
from api.v1.views import app_views
from os import getenv
from flask_cors import CORS
from flasgger import Swagger

app = Flask(__name__)
app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown(exc):
    """closing"""
    storage.close()


CORS(app, resources={r"/*": {"origins": "0.0.0.0"}})
app.config['SWAGGER'] = {
    "swagger_version": "2.0",
    "title": "Flasgger",
    "headers": [
        ('Access-Control-Allow-Origin', '*'),
        ('Access-Control-Allow-Methods', "GET, POST, PUT, DELETE, OPTIONS"),
        ('Access-Control-Allow-Credentials', "true"),
    ],
    "specs": [
        {
            "version": "1.0",
            "title": "HBNB API",
            "endpoint": 'v1_views',
            "description": 'HBNB REST API',
            "route": '/v1/views',
        }
    ]
}
swagger = Swagger(app)

@app.errorhandler(404)
def not_found(error):
    """json return"""
    return make_response(jsonify({"error": "Not found"}), 404)




if __name__ == "__main__":
    HBNB_API_HOST = getenv('HBNB_API_HOST')
    HBNB_API_PORT = getenv('HBNB_API_PORT')

    host = "0.0.0.0" if not HBNB_API_HOST else HBNB_API_HOST
    port = 5000 if not HBNB_API_PORT else HBNB_API_PORT

    app.run(host=host, port=port, threaded=True)
