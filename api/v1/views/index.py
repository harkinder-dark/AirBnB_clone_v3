"""
create a file index.py
import app_views from api.v1.views
create a route /status on the object app_views
that returns a JSON: "status": "OK" (see example)
"""
from api.v1.views import app_views
from flask import jsonify


@app_views.route('/status',  methods=['GET'], strict_slashes=False)
def status():
    """Returns JSON"""
    return jsonify({"status": "OK"})
