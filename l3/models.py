from datetime import datetime
from bson import ObjectId

from database import users_collection, policies_collection, claims_collection


class User:
    def __init__(self, username, role="user"):
        self.username = username
        self.role = role
        self.created_at = datetime.utcnow()

    def save(self):
        user_doc = {
            "username": self.username,
            "role": self.role,
            "created_at": self.created_at
        }
        result = users_collection.insert_one(user_doc)
        return result.inserted_id


class InsurancePolicy:
    def __init__(self, policy_name, coverage_amount, user_id):
        self.policy_name = policy_name
        self.coverage_amount = coverage_amount
        self.user_id = user_id
        self.created_at = datetime.utcnow()

    def save(self):
        policy_doc = {
            "policy_name": self.policy_name,
            "coverage_amount": self.coverage_amount,
            "user_id": self.user_id,
            "created_at": self.created_at
        }
        result = policies_collection.insert_one(policy_doc)
        return result.inserted_id


class Claim:
    def __init__(self, policy_id, claim_amount, status="Pending"):
        self.policy_id = policy_id
        self.claim_amount = claim_amount
        self.status = status
        self.created_at = datetime.utcnow()

    def save(self):
        claim_doc = {
            "policy_id": self.policy_id,
            "claim_amount": self.claim_amount,
            "status": self.status,
            "created_at": self.created_at
        }
        result = claims_collection.insert_one(claim_doc)
        return result.inserted_id

