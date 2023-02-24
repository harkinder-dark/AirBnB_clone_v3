#!/usr/bin/python3
"""
Create a new view for State objects that handles all
Updates a State object: PUT /api/v1/states/<state_id>
"""
from flask import jsonify, request
from api.v1.views import app_views
from models import storage
from models.state import State
from flask import abort, make_response


@app_views.route('/states', method=['GET'], strict_slashes=False)
def states():
    """objects that handles all default RESTFul API actions"""
    state = storage.all(State)
    return jsonify([obj.to_dict() for obj in state.values()])


@app_views.route('/states/<state_id>', method=['GET'],
                  strict_slashes=False)
def f_state_id(state_id):
    """Retrieves a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    return jsonify(state.to_dict())


@app_views.route('/states/<state_id>', method=['DELETE'],
                 strict_slashes=False)
def d_state_id(state_id):
    """Deletes a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', method=['POST'], strict_slashes=False)
def post_states():
    """You must use request.get_json from Flas"""
    new = request.get_json()
    if not new:
        abort(400, "Not a JSON")
    if 'name' not in new:
        abort(400, "Missing name")
    state = State(**new)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('/states/<state_id>', method=['PUT'],
                 strict_slashes=False)
def put_states(state_id):
    """Updates a State object"""
    state = storage.get(State, state_id)
    if not state:
        abort(404)
    chnew = request.get_json()
    if not chnew:
        abort(400, "Not a JSON")
    for key, val in chnew:
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(state, key, val)
    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
