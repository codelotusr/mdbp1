from bson.objectid import ObjectId
from flask import Blueprint, jsonify, request

from models.database import movies_collection, studios_collection

studios_bp = Blueprint("studios", __name__)


@studios_bp.route("/studios", methods=["POST"])
def create_studio():
    data = request.get_json()

    if not data or not data.get("name"):
        return jsonify({"error": "Studio name is required"}), 400

    studio = {
        "name": data["name"].strip().title(),
        "year_founded": data.get("year_founded"),
        "headquarters": data.get("headquarters", {}),
        "movies_produced": [],
    }

    result = studios_collection.insert_one(studio)

    return (
        jsonify(
            {"message": "Studio added successfully", "id": str(result.inserted_id)}
        ),
        201,
    )


@studios_bp.route("/studios", methods=["GET"])
def get_studios():
    studios = list(
        studios_collection.find(
            {}, {"_id": 1, "name": 1, "year_founded": 1, "headquarters": 1}
        )
    )

    for studio in studios:
        studio["_id"] = str(studio["_id"])

    return jsonify(studios)


@studios_bp.route("/studios/<string:studio_id>/add_movie", methods=["PUT"])
def add_movie_to_studio(studio_id):
    try:
        if not ObjectId.is_valid(studio_id):
            return jsonify({"error": "Invalid ObjectId format"}), 400

        studio_object_id = ObjectId(studio_id)

        existing_studio = studios_collection.find_one({"_id": studio_object_id})
        if not existing_studio:
            return jsonify({"error": "Studio not found"}), 404

        data = request.get_json()
        if not data or not data.get("movie_id"):
            return jsonify({"error": "Movie ID is required"}), 400

        movie_id = data["movie_id"]

        existing_movie = movies_collection.find_one({"_id": ObjectId(movie_id)})
        if not existing_movie:
            return jsonify({"error": "Movie not found"}), 404

        studios_collection.update_one(
            {"_id": studio_object_id},
            {"$addToSet": {"movies_produced": ObjectId(movie_id)}},
        )

        return jsonify({"message": "Movie added to studio successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@studios_bp.route("/studios/<string:studio_id>", methods=["PUT"])
def update_studio(studio_id):
    try:
        if not ObjectId.is_valid(studio_id):
            return jsonify({"error": "Invalid ObjectId format"}), 400

        studio_object_id = ObjectId(studio_id)

        existing_studio = studios_collection.find_one({"_id": studio_object_id})
        if not existing_studio:
            return jsonify({"error": "Studio not found"}), 404

        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid or missing JSON data"}), 400

        update_query = {"$set": data}
        studios_collection.update_one({"_id": studio_object_id}, update_query)

        return jsonify({"message": "Studio updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@studios_bp.route("/studios/<string:studio_id>", methods=["DELETE"])
def delete_studio(studio_id):
    try:
        if not ObjectId.is_valid(studio_id):
            return jsonify({"error": "Invalid ObjectId format"}), 400

        studio_object_id = ObjectId(studio_id)

        existing_studio = studios_collection.find_one({"_id": studio_object_id})
        if not existing_studio:
            return jsonify({"error": "Studio not found"}), 404

        studios_collection.delete_one({"_id": studio_object_id})

        return jsonify({"message": "Studio deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
