from datetime import datetime
from zoneinfo import ZoneInfo

from bson.objectid import ObjectId
from flask import Blueprint, jsonify, request

from models.database import genres_collection

genres_bp = Blueprint("genres", __name__)


@genres_bp.route("/genres", methods=["POST"])
def create_genre():
    data = request.get_json()

    if not data or not data.get("name"):
        return jsonify({"error": "Genre name is required"}), 400

    genre = {
        "name": data["name"].strip().title(),
        "description": data.get("description", ""),
        "created_at": datetime.now(ZoneInfo("Europe/Vilnius")),
    }

    result = genres_collection.insert_one(genre)

    return (
        jsonify({"message": "Genre added successfully", "id": str(result.inserted_id)}),
        201,
    )


@genres_bp.route("/genres", methods=["GET"])
def get_genres():
    genres = list(genres_collection.find({}, {"_id": 1, "name": 1, "description": 1}))

    for genre in genres:
        genre["_id"] = str(genre["_id"])

    return jsonify(genres)


@genres_bp.route("/genres/<string:genre_id>", methods=["PUT"])
def update_genre(genre_id):
    try:
        if not ObjectId.is_valid(genre_id):
            return jsonify({"error": "Invalid ObjectId format"}), 400

        genre_object_id = ObjectId(genre_id)

        existing_genre = genres_collection.find_one({"_id": genre_object_id})
        if not existing_genre:
            return jsonify({"error": "Genre not found"}), 404

        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid or missing JSON data"}), 400

        if not any(data.values()):
            return jsonify({"error": "No valid fields provided for update"}), 400

        update_query = {"$set": data}
        genres_collection.update_one({"_id": genre_object_id}, update_query)

        return jsonify({"message": "Genre updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@genres_bp.route("/genres/<string:genre_id>", methods=["DELETE"])
def delete_genre(genre_id):
    try:
        if not ObjectId.is_valid(genre_id):
            return jsonify({"error": "Invalid ObjectId format"}), 400

        genre_object_id = ObjectId(genre_id)

        existing_genre = genres_collection.find_one({"_id": genre_object_id})
        if not existing_genre:
            return jsonify({"error": "Genre not found"}), 404

        genres_collection.delete_one({"_id": genre_object_id})

        return jsonify({"message": "Genre deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
