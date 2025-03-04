from database import Base, engine
from models import User

# Створення таблиць
Base.metadata.create_all(bind=engine)
print("База даних створена")
