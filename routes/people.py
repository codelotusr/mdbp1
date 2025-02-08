from bson.objectid import ObjectId
from flask import Blueprint, jsonify, request

from models.database import people_collection

people_bp = Blueprint("people", __name__)


@people_bp.route("/people", methods=["GET"])
def get_people():
    people = list(people_collection.find({}, {"_id": 0}))
    return jsonify(people)


@people_bp.route("/people", methods=["POST"])
def create_person():
    data = request.json
    if not data.get("first_name") or not data.get("last_name"):
        return jsonify({"error": "Missing required fields"}), 400

    result = people_collection.insert_one(data)
    return (
        jsonify(
            {"message": "Person added successfully", "id": str(result.inserted_id)}
        ),
        201,
    )


@people_bp.route("/people/<string:person_id>", methods=["PUT"])
def update_person(person_id):
    data = request.json
    if not data:
        return jsonify({"error": "No update data provided"}), 400

    update_query = {"$set": data}

    result = people_collection.update_one({"_id": ObjectId(person_id)}, update_query)

    if result.matched_count == 0:
        return jsonify({"error": "Person not found"}), 404

    return jsonify({"message": "Person updated successfully"}), 200


@people_bp.route("/people/<string:person_id>", methods=["DELETE"])
def delete_person(person_id):
    result = people_collection.delete_one({"_id": ObjectId(person_id)})

    if result.deleted_count == 0:
        return jsonify({"error": "Person not found"}), 404

    return jsonify({"message": "Person deleted successfully"}), 200
