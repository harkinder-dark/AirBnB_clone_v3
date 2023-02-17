#!/usr/bin/python3
"""create a file index.py"""
from api.v1.views import app_views
from flask import jsonify
from models import storage


@app_views.route('/status',  methods=['GET'], strict_slashes=False)
def status():
    """Returns JSON"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'], strict_slashes=False)
def get_stats():
    classes = {
        "amenities": "Amenity",
        "cities": "City",
        "places": "Place",
        "reviews": "Review",
        "states": "State",
        "users": "User"
    }
    stats = {}
    for key, value in classes.items():
        stats[key] = storage.count(value)
    return jsonify(stats)
