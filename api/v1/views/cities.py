#!/usr/bin/python3
"""
Same as State, create a new view for City objects
        that handles all default RESTFul API actions:
Retrieves the list of all City objects of a State

"""
from flask import Flask, jsonify, abort
from api.v1.views import app_views
from models import storage
from models.state import State
from models.city import City
from flask import make_response, request


@app_views.route('/states/<state_id>/cities', method=['GET'],
                 strict_slashes=False)
def cities(state_id):
    """Retrieves the list of all City objects
    of a State:"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify([obj.to_dict() for obj in state.cities])


@app_views.route('/cities/<city_id>', method=['GET'],
                 strict_slashes=False)
def get_city(city_id):
    """Retrieves a City object"""
    citie = storage.get(City, city_id)
    if not citie:
        abort(404)
    return jsonify(citie.to_dict())


@app_views.route('/cities/<city_id>', method=['DELETE'],
                 strict_slashes=False)
def del_city(city_id):
    """Deletes a City object:"""
    citie = storage.get(City, city_id)
    if not citie:
        abort(404)
    citie.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', method=['POST'],
                 strict_slashes=False)
def post_city(state_id):
    """Creates a City"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    new_city = request.get_json()
    if not new_city:
        abort(400, "Not a JSON")
    if 'name' not in new_city:
        abort(400, "Missing name")
    citie = City(**new_city)
    storage.save()
    return make_response(jsonify(citie.to_dict()), 201)


@app_views.route('/cities/<city_id>', method=['PUT'],
                 strict_slashes=False)
def put_city(city_id):
    """Updates a City object"""
    citie = storage.get(City, city_id)
    if not citie:
        abort(404)
    chcity = request.get_json()
    if not chcity:
        abort(400, "Not a JSON")
    for key, val in chcity:
        if key not in ['id', 'created_at', 'updated_at', 'state_id']:
            setattr(citie, key, val)
    storage.save()
    return make_response(jsonify(citie.to_dict()), 200)
