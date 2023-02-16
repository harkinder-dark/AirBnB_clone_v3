"""
GET
DELETE
POST
PUT
"""
from flask import Flask, jsonify
from api.v1.views import app_views
from models import storage
from models.place import Place
from models.city import City
from models.user import User
from flask import abort
from flask import make_response
from flask import request


@app_views.route('/cities/<city_id>/places', method=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """get all Place to city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    return jsonify([obj.to_dict() for obj in city.places])


@app_views.route('/places/<place_id>', method=['GET'],
                 strict_slashes=False)
def placeid(place_id):
    """get place element"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<place_id>', method=['DELETE'],
                 strict_slashes=False)
def del_place(place_id):
    """delete place element"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    place.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/cities/<city_id>/places', method=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """post place to city"""
    city = storage.get(City, city_id)
    if not city:
        abort(404)
    new_place = request.get_json()
    if not new_place:
        abort(400, "Not a JSON")
    if 'user_id' not in new_place:
        abort(400, "Missing user_id")
    user_id = new_place['user_id']
    if not storage.get(User, user_id):
        abort(404)
    if 'name' not in new_place:
        abort(400, "Missing name")
    place = Place(**new_place)
    setattr(place, 'city_id', city_id)
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<place_id>',method=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """modified"""
    place = storage.get(Place, place_id)
    if not place:
        abort(404)
    chplace = request.get_json()
    if not chplace:
        abort(400, "Not a JSON")
    for key, val in chplace:
        if key not in ['id', 'user_id', 'city_id', 'created_at',
                       'updated_at']:
            setattr(place, key, val)
    storage.save()
    return make_response(jsonify(place.to_dict()), 200)


@app_views.route('/places_search', method=['POST'],
                 strict_slashes=False)
def places_search():
    """Good, but not enough"""
    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")
    
    if body is None or (
            not body.get('states') and
            not body.get('cities') and
            not body.get('amenities')
    ):
    places = storage.all(Place)
    return jsonify([place.to_dict() for place in palces.values()])
