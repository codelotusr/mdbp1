from bson.objectid import ObjectId
from flask import Blueprint, jsonify, request

from models.database import awards_collection, movies_collection, people_collection

awards_bp = Blueprint("awards", __name__)


@awards_bp.route("/awards", methods=["POST"])
def create_award():
    data = request.get_json()

    if (
        not data
        or not data.get("name")
        or not data.get("category")
        or not data.get("year")
        or not data.get("recipient_type")
        or not data.get("recipient_id")
    ):
        return jsonify({"error": "Missing required fields"}), 400

    recipient_id = data["recipient_id"]
    recipient_type = data["recipient_type"]

    if recipient_type not in ["movie", "person"]:
        return (
            jsonify({"error": "Invalid recipient_type. Must be 'movie' or 'person'"}),
            400,
        )

    if recipient_type == "movie":
        if not movies_collection.find_one({"_id": ObjectId(recipient_id)}):
            return jsonify({"error": "Movie not found"}), 404
    elif recipient_type == "person":
        if not people_collection.find_one({"_id": ObjectId(recipient_id)}):
            return jsonify({"error": "Person not found"}), 404

    award = {
        "name": data["name"].strip(),
        "category": data["category"].strip(),
        "year": data["year"],
        "recipient_type": recipient_type,
        "recipient_id": ObjectId(recipient_id),
        "won": data.get("won", False),
    }

    result = awards_collection.insert_one(award)
    return (
        jsonify({"message": "Award added successfully", "id": str(result.inserted_id)}),
        201,
    )


@awards_bp.route("/awards", methods=["GET"])
def get_awards():
    awards = list(
        awards_collection.find(
            {},
            {
                "_id": 1,
                "name": 1,
                "category": 1,
                "year": 1,
                "recipient_type": 1,
                "recipient_id": 1,
                "won": 1,
            },
        )
    )

    for award in awards:
        award["_id"] = str(award["_id"])
        award["recipient_id"] = str(award["recipient_id"])

    return jsonify(awards)


@awards_bp.route("/awards/<string:award_id>", methods=["PUT"])
def update_award(award_id):
    try:
        if not ObjectId.is_valid(award_id):
            return jsonify({"error": "Invalid ObjectId format"}), 400

        award_object_id = ObjectId(award_id)

        existing_award = awards_collection.find_one({"_id": award_object_id})
        if not existing_award:
            return jsonify({"error": "Award not found"}), 404

        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid or missing JSON data"}), 400

        update_query = {"$set": data}
        awards_collection.update_one({"_id": award_object_id}, update_query)

        return jsonify({"message": "Award updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@awards_bp.route("/awards/<string:award_id>", methods=["DELETE"])
def delete_award(award_id):
    try:
        if not ObjectId.is_valid(award_id):
            return jsonify({"error": "Invalid ObjectId format"}), 400

        award_object_id = ObjectId(award_id)

        existing_award = awards_collection.find_one({"_id": award_object_id})
        if not existing_award:
            return jsonify({"error": "Award not found"}), 404

        awards_collection.delete_one({"_id": award_object_id})

        return jsonify({"message": "Award deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
