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

    people_collection.insert_one(data)
    return jsonify({"message": "Person added successfully"}), 200
