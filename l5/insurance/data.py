class User:
    def __init__(self, id, name, role):
        self.id = id
        self.name = name
        self.role = role

class Policy:
    def __init__(self, id, user_id, coverage):
        self.id = id
        self.user_id = user_id
        self.coverage = coverage

class Claim:
    def __init__(self, id, policy_id, amount):
        self.id = id
        self.policy_id = policy_id
        self.amount = amount


# Фіксовані дані у вигляді списків:
users = [
    User(4, 'Ivan Petrov', 'admin'),
    User(5, 'Olena Shevchenko', 'user'),
]

policies = [
    Policy(4, 4, 100000),
    Policy(5, 5, 50000),
]

claims = [
    Claim(4, 4,  10000),
    Claim(5, 5,  20000),
]


