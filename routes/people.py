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
    data = request.get_json()

    if not data:
        return jsonify({"error": "Invalid or missing JSON data"}), 400

    if not data.get("first_name") or not data.get("last_name"):
        return jsonify({"error": "Missing required fields"}), 400

    person = {
        "first_name": data["first_name"],
        "last_name": data["last_name"],
        "birth_date": data.get("birth_date"),
        "roles": data.get("roles", []),
    }

    result = people_collection.insert_one(person)
    return (
        jsonify(
            {"message": "Person added successfully", "id": str(result.inserted_id)}
        ),
        201,
    )


@people_bp.route("/people/<string:person_id>", methods=["PUT"])
def update_person(person_id):
    try:
        if not ObjectId.is_valid(person_id):
            return jsonify({"error": "Invalid ObjectId format"}), 400

        person_object_id = ObjectId(person_id)

        existing_person = people_collection.find_one({"_id": person_object_id})
        if not existing_person:
            return jsonify({"error": "Person not found"}), 404

        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid or missing JSON data"}), 400

        if not any(data.values()):
            return jsonify({"error": "No valid fields provided for update"}), 400

        result = people_collection.update_one({"_id": person_object_id}, {"$set": data})

        if result.modified_count == 0:
            return jsonify({"message": "No changes made. The data is the same."}), 200

        return jsonify({"message": "Person updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@people_bp.route("/people/<string:person_id>", methods=["DELETE"])
def delete_person(person_id):
    try:
        if not ObjectId.is_valid(person_id):
            return jsonify({"error": "Invalid ObjectId format"}), 400

        person_object_id = ObjectId(person_id)

        existing_person = people_collection.find_one({"_id": person_object_id})
        if not existing_person:
            return jsonify({"error": "Person not found"}), 404

        people_collection.delete_one({"_id": person_object_id})

        return jsonify({"message": "Person deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
