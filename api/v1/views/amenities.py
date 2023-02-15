"""
"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity
from flask import abort
from flask import make_response
from flask import request


@app_views.route('/amenities', method=['GET'],
                 strict_slashes=False)
def amenities():
    """list all elements"""
    d_amenities = storage.all(Amenity)
    return jsonify([obj.to_dict() for obj in d_amenities.values()])


@app_views.route('/amenities/<amenity_id>', method=['GET'],
                 strict_slashes=False)
def amenity(amenity_id):
    """get element by id"""
    amenityId = storage.get(Amenity, amenity_id)
    if not amenityId:
        abort(404)
    return jsonify(amenityId.to_dict())


@app_views.route('/amenities/<amenity_id>', method=['DELETE'],
                 strict_slashes=False)
def del_amenity(amenity_id):
    """delete element"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenityId:
        abort(404)
    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/amenities', method=['POST'], strict_slashes=False)
def post_amenity():
    """add new element"""
    new_amenity = request.get_json()
    if not new_amenity:
        abort(400, "Not a JSON")
    if 'name' in not new_amenity:
        abort(400, "Missing name")
    amenity = Amenity(**new_amenity)
    storage.new(amenity)
    storage.save()
    return make_response(jsonify(amenity/to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', method=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """modified database"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    chamenity = request.get_json()
    if not chamenity:
        abort(400, "Not a JSON")
    for key, val in chamenity:
        if key not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, key, val)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
