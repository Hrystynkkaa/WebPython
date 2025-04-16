from pymongo import MongoClient

# Підключення до MongoDB
client = MongoClient("mongodb://localhost:27017/")
mongo_db = client["lab3"]

# Колекції для MongoDB
users_collection = mongo_db["users"]
policies_collection = mongo_db["policies"]
claims_collection = mongo_db["claims"]

