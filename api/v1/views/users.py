#!/usr/bin/python3
"""
Create a new view for User object
Retrieves the list of all User objects
Retrieves a User object
Deletes a User object
Creates a User
Updates a User object
"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from models.user import User
from flask import abort
from flask import make_response
from flask import request


@app_views.route('/users', method=['GET'], strict_slashes=False)
def users():
    """list all elemets"""
    user = storage.all(User)
    return jsonify([obj.to_dict() for obj in user.values()])


@app_views.rouute('/users/<user_id>', method=['GET'],
                  strict_slashes=False)
def get_user(user_id):
    """get elements by id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', method=['DELETE'],
                 strict_slashes=False)
def del_user(user_id):
    """delete element by id"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    user.delete()
    user.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', method=['POST'], strict_slashes=False)
def post_users():
    """add element"""
    new_user = request.get_json()
    if not new_user:
        abort(400, "Not a JSON")
    if 'email' not in new_user:
        abort(400, "Missing email")
    if 'password' not in new_user:
        abort(400, "Missing password")
    user = User(**new_user)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', method=['PUT'],
                 strict_slashes=False)
def put_user(user_id):
    """modified"""
    user = storage.get(User, user_id)
    if not user:
        abort(404)
    new_user = request.get_json()
    if not new_user:
        abort(400, "Not a JSON")
    for key, val in new_user:
        if key not in ['id', 'email', 'created_at', 'updated_at']:
            setattr(user, key, val)
    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
