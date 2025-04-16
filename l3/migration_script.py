from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from pymongo import MongoClient
from models import User, InsurancePolicy, Claim
from database import Base
from bson import ObjectId

# Підключення до PostgreSQL
DATABASE_URL = "postgresql://postgres:Hristina@localhost/lab2"
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db_session = SessionLocal()

# Підключення до MongoDB
client = MongoClient("mongodb://localhost:27017/")
mongo_db = client["lab3"]

# Створення колекцій MongoDB
users_collection = mongo_db["users"]
policies_collection = mongo_db["policies"]
claims_collection = mongo_db["claims"]

# Очистка колекцій MongoDB перед міграцією
users_collection.delete_many({})
policies_collection.delete_many({})
claims_collection.delete_many({})

# Міграція користувачів з PostgreSQL в MongoDB
postgres_to_mongo_user_ids = {}  # {int_id: inserted_id(ObjectId)}

for user in db_session.query(User).all():
    user_doc = {
        "_id": ObjectId(),  # MongoDB автоматично створить ObjectId
        "username": user.username,
        "role": user.role,
    }
    # Вставка документа у MongoDB
    users_collection.insert_one(user_doc)
    postgres_to_mongo_user_ids[user.id] = user_doc["_id"]

# Міграція страхових полісів з PostgreSQL в MongoDB
postgres_to_mongo_policy_ids = {}  # {int_id: inserted_id(ObjectId)}

for policy in db_session.query(InsurancePolicy).all():
    # Отримуємо новий _id користувача
    mongo_user_id = postgres_to_mongo_user_ids[policy.user_id]

    policy_doc = {
        "_id": ObjectId(),  # MongoDB автоматично створить ObjectId
        "policy_name": policy.policy_name,
        "coverage_amount": policy.coverage_amount,
        "user_id": mongo_user_id,  # використовуємо новий ObjectId користувача
    }
    # Вставка документа в MongoDB
    policies_collection.insert_one(policy_doc)
    postgres_to_mongo_policy_ids[policy.id] = policy_doc["_id"]

# Міграція заяв з PostgreSQL в MongoDB
for claim in db_session.query(Claim).all():
    # Отримуємо новий _id поліса
    mongo_policy_id = postgres_to_mongo_policy_ids[claim.policy_id]

    claim_doc = {
        "policy_id": mongo_policy_id,  # посилання на поліс з MongoDB
        "claim_amount": claim.claim_amount,
        "status": claim.status,
    }
    # Вставка документа в MongoDB
    claims_collection.insert_one(claim_doc)

db_session.close()

print("Міграція даних завершена")


