from bson.objectid import ObjectId
from flask import Blueprint, jsonify, request

from models.database import movies_collection, people_collection, studios_collection

movies_bp = Blueprint("movies", __name__)


@movies_bp.route("/movies", methods=["POST"])
def create_movie():
    data = request.get_json()

    if not data or not data.get("title") or not data.get("release_year"):
        return jsonify({"error": "Title and release year are required"}), 400

    director_id = data.get("director_id")
    studio_id = data.get("studio_id")
    actors = data.get("actors", [])

    if director_id and not people_collection.find_one({"_id": ObjectId(director_id)}):
        return jsonify({"error": "Director not found"}), 404

    if studio_id and not studios_collection.find_one({"_id": ObjectId(studio_id)}):
        return jsonify({"error": "Studio not found"}), 404

    validated_actors = []
    for actor in actors:
        person_id = actor.get("person_id")
        role = actor.get("as", "")

        if not people_collection.find_one({"_id": ObjectId(person_id)}):
            return jsonify({"error": f"Actor with ID {person_id} not found"}), 404

        validated_actors.append({"person_id": ObjectId(person_id), "as": role})

    movie = {
        "title": data["title"].strip(),
        "director_id": ObjectId(director_id) if director_id else None,
        "release_year": data["release_year"],
        "imdb": data.get("imdb", {}),
        "actors": validated_actors,
        "studio_id": ObjectId(studio_id) if studio_id else None,
    }

    result = movies_collection.insert_one(movie)
    return (
        jsonify({"message": "Movie added successfully", "id": str(result.inserted_id)}),
        201,
    )


@movies_bp.route("/movies", methods=["GET"])
def get_movies():
    movies = list(
        movies_collection.find({}, {"_id": 1, "title": 1, "release_year": 1, "imdb": 1})
    )

    for movie in movies:
        movie["_id"] = str(movie["_id"])

    return jsonify(movies)


@movies_bp.route("/movies/<string:movie_id>", methods=["PUT"])
def update_movie(movie_id):
    try:
        if not ObjectId.is_valid(movie_id):
            return jsonify({"error": "Invalid ObjectId format"}), 400

        movie_object_id = ObjectId(movie_id)

        existing_movie = movies_collection.find_one({"_id": movie_object_id})
        if not existing_movie:
            return jsonify({"error": "Movie not found"}), 404

        data = request.get_json()
        if not data:
            return jsonify({"error": "Invalid or missing JSON data"}), 400

        update_query = {"$set": data}
        movies_collection.update_one({"_id": movie_object_id}, update_query)

        return jsonify({"message": "Movie updated successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


@movies_bp.route("/movies/<string:movie_id>", methods=["DELETE"])
def delete_movie(movie_id):
    try:
        if not ObjectId.is_valid(movie_id):
            return jsonify({"error": "Invalid ObjectId format"}), 400

        movie_object_id = ObjectId(movie_id)

        existing_movie = movies_collection.find_one({"_id": movie_object_id})
        if not existing_movie:
            return jsonify({"error": "Movie not found"}), 404

        movies_collection.delete_one({"_id": movie_object_id})

        return jsonify({"message": "Movie deleted successfully"}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
