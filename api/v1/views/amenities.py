#!/usr/bin/python3
"""API actions for Amenity objects"""
from flask import jsonify, request, abort
from api.v1.views import app_views
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities',
                 methods=['GET'], strict_slashes=False)
def get_amenities():
    """Retrieves the list of all Amenity objects"""
    amenities = [amenity.to_dict() for amenity in storage.all(Amenity).values()]
    return jsonify(amenities)


@app_views.route('/amenities/<amenity_id>',
                 methods=['GET'], strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity(amenity_id):
    """Deletes an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)
    storage.delete(amenity)
    storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def create_amenity():
    """Creates a new Amenity"""
    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")
    if 'name' not in data:
        abort(400, description="Missing name")

    new_amenity = Amenity(**data)
    storage.new(new_amenity)
    storage.save()
    return jsonify(new_amenity.to_dict()), 201


@app_views.route('/amenities/<amenity_id>', methods=['PUT'], strict_slashes=False)
def update_amenity(amenity_id):
    """Updates an Amenity object"""
    amenity = storage.get(Amenity, amenity_id)
    if not amenity:
        abort(404)

    data = request.get_json(silent=True)
    if data is None:
        abort(400, description="Not a JSON")

    ignored_keys = ['id', 'created_at', 'updated_at']
    for key, value in data.items():
        if key not in ignored_keys:
            setattr(amenity, key, value)

    storage.save()
    return jsonify(amenity.to_dict()), 200
