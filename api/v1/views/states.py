#!/usr/bin/python3
"""
Create a new view for State objects that handles all
                        default RESTFul API actions:
Retrieves the list of all State objects: GET /api/v1/states
Retrieves a State object: GET /api/v1/states/<state_id>
Deletes a State object:: DELETE /api/v1/states/<state_id>
Creates a State: POST /api/v1/states
Updates a State object: PUT /api/v1/states/<state_id>
"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort
from flask import make_response
from flask import request


@app_views.route('/states', method=['GET'], strict_slashes=False)
def states():
    """objects that handles all default RESTFul API actions"""
    state = storage.all(State)
    return jsonify([obj.to_dict() for obj in state.values()])


@app_views.route('/states/<state_id>', method=['GET'],
                  strict_slashes=False)
def f_state_id(state_id):
    """Retrieves a State object"""
    stateid = storage.get("State", state_id)
    if not stateid:
        abort(404)
    return jsonify(stateid.to_dict())


@app_views.route('/states/<state_id>', method=['DELETE'],
                 strict_slashes=False)
def d_state_id(state_id):
    """Deletes a State object"""
    stateid = storage.get("State", state_id)
    if not stateid:
        abort(404)
    stateid.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', method=['POST'], strict_slashes=False)
def post_states():
    """You must use request.get_json from Flas"""
    new = request.get_json()
    if not new:
        abort(404, "Not a JSON")
    if 'name' not in new:
        abort(400, "Missing name")
    state = State(**new)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', method=['PUT'],
                 strict_slashes=False)
def put_states(state_id):
    """Updates a State object"""
    stateid = storage.get("State", state_id)
    if not stateid:
        abort(404)
    chnew = request.get_json()
    if not chnew:
        abort(400, "Not a JSON")
    for key, val in chnew:
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(stateid, key, val)
    storage.save()
    return make_response(jsonify(stateid.to_dict()), 200)
