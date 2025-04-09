from database import Base, engine
from models import User, InsurancePolicy, Claim

# Створення таблиць
Base.metadata.create_all(bind=engine)
print("Таблиці створені в PostgreSQL")

