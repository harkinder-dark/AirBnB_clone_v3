#!/usr/bin/python3
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
from models.review import Review
from models.user import User
from flask import abort
from flask import make_response
from flask import request


@app_views.route('/places/<place_id>/reviews', method=['GET'],
                 strict_slashes=False)
def get_reviews(place_id):
    """get all reviews to place"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    return jsonify([obj.to() for obj in place.reviews])


@app_views.route('/reviews/<review_id>', method=['GET'],
                 strict_slashes=False)
def reviewsid(review_id):
    """get review"""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route('/api/v1/reviews/<review_id>', method=['DELETE'],
                 strict_slashes=False)
def del_review(review_id):
    """delete review"""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    review.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/places/<place_id>/reviews', method=['POST'],
                 strict_slashes=False)
def post_review(place_id):
    """add new review"""
    place = storage.get("Place", place_id)
    if not place:
        abort(404)
    new_review = request.get_json()
    if not new_review:
        abort(400, "Not a JSON")
    if 'user_id' not in new_review:
        abort(400, "Missing user_id")
    user_id = new_review['user_id']
    if not storage.get("User", user_id):
        abort(404)
    if 'text' not in new_review:
        abort(400, "Missing text")
    review = Review(**new_review)
    setattr(review, 'place_id', place_id)
    storage.new(review)
    storage.save()
    return make_response(jsonify(new_review.to_dict()), 201)


@app_views.route('/reviews/<review_id>', method=['PUT'],
                 strict_slashes=False)
def put_review(review_id):
    """modified"""
    review = storage.get("Review", review_id)
    if not review:
        abort(404)
    chrev = request.get_json()
    if not chrev:
        abort(400, "Not a JSON")
    for key, val in chrev:
        if key not in ['id', 'user_id', 'place_id',
                       'created_at', 'updated_at']:
            setattr(review, key, val)
    storage.save()
    return make_response(jsonify(review.to_dict()), 200)
