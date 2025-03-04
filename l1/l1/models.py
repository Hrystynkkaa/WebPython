from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    role = Column(String, default="user")  # "admin" або "user"

class InsurancePolicy(Base):
    __tablename__ = "policies"

    id = Column(Integer, primary_key=True, index=True)
    policy_name = Column(String, index=True)
    coverage_amount = Column(Integer)
    user_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User")

class Claim(Base):
    __tablename__ = "claims"

    id = Column(Integer, primary_key=True, index=True)
    policy_id = Column(Integer, ForeignKey("policies.id"))
    claim_amount = Column(Integer)
    status = Column(String, default="Pending")

    policy = relationship("InsurancePolicy")
