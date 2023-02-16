"""
GET
DELETE
POST
"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.amenity import Amenity
from flask import abort
from flask import make_response
from flask import request


@app_views.route('/places/<place_id>/amenities', method=['GET'],
                 strict_slashes=False)
def get_places_amenities(place_id):
    """get element"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        l = [amenity.to_dict() for amenity in place.amenities]
    else:
        l = [storage.get("Amenity", id).to_dict() for id in place.amenity_ids]
    return jsonify(l)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 method=['DELETE'], strict_slashes=False)
def del_places_amenities(place_id, amenity_id):
    """deleting"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity not in place.amenities:
            abort(404)
    else:
        if amenity_id not in place.amenity_ids:
            abort(404)
        index = place.amenity_ids.index(amenity_id)
        place.amenity_ids.pop(index)

    amenity.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/amenities/<amenity_id>',
                 method=['POST'], strict_slashes=False)
def post_places_amenities(place_id, amenity_id):
    """add"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    if getenv('HBNB_TYPE_STORAGE') == 'db':
        if amenity in place.amenities:
            return make_response(jsonify(amenity.to_dict()), 200)
        place.amenities.append(amenity)
    else:
        if amenity_id in place.amenity_ids:
            return make_response(jsonify(amenity.to_dict()), 200)
        place.amenity_ids.append(amenity_id)

    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)
