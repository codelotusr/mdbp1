from pymongo.mongo_client import MongoClient

client = MongoClient("mongodb://localhost:27017/")

db = client["mdbpDb"]

people_collection = db["People"]
movies_collection = db["Movies"]
studios_collection = db["Studios"]
