# insurance/data.py

class User:
    def __init__(self, username, role):
        self.username = username
        self.role = role

class InsurancePolicy:
    def __init__(self, id, name, amount, owner):
        self.id = id
        self.name = name
        self.amount = amount
        self.owner = owner

class Claim:
    def __init__(self, amount, policy):
        self.amount = amount
        self.policy = policy

# Фіксовані користувачі
USERS = [
    User("user1", "user"),
    User("admin1", "admin"),
]

# Поліси
POLICIES = [
    InsurancePolicy(1, "Health Insurance", 100000, USERS[0]),
    InsurancePolicy(2, "Life Insurance", 200000, USERS[1]),
]

# Заяви
CLAIMS = [
    Claim(5000, POLICIES[0]),
    Claim(10000, POLICIES[1]),
]
