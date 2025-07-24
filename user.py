import json
import os

USERS_FILE = "data/users.json"


class User:
    def __init__(self, username, role='customer'):
        self.username = username
        self.role = role

    @staticmethod
    def load_users():
        if not os.path.exists(USERS_FILE):
            return {}
        with open(USERS_FILE) as f:
            return json.load(f)

    @staticmethod
    def save_users(users):
        with open(USERS_FILE, 'w') as f:
            json.dump(users, f, indent=2)

    @staticmethod
    def login(username, password):
        users = User.load_users()
        if username in users and users[username]["password"] == password:
            return User(username, users[username]["role"])
        return None

    @staticmethod
    def register(username, password, role="customer"):
        users = User.load_users()
        if username in users:
            print(" Username already exists.")
            return None
        users[username] = {"password": password, "role": role, "balance": 0}
        User.save_users(users)
        print(" Registration successful.")
        return User(username, role)
