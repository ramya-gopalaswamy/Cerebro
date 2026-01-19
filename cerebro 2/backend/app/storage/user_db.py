"""File-based user database for authentication."""
import json
import os
from typing import Optional, Dict
from pydantic import EmailStr

USER_DB_PATH = os.path.join(os.path.dirname(__file__), "users.json")

class UserDB:
    def __init__(self, db_path: str = USER_DB_PATH):
        self.db_path = db_path
        if not os.path.exists(self.db_path):
            with open(self.db_path, "w") as f:
                json.dump({}, f)

    def load_users(self) -> Dict[str, Dict]:
        with open(self.db_path, "r") as f:
            return json.load(f)

    def save_users(self, users: Dict[str, Dict]):
        with open(self.db_path, "w") as f:
            json.dump(users, f, indent=2)

    def get_user(self, email: EmailStr) -> Optional[Dict]:
        users = self.load_users()
        return users.get(email)

    def add_user(self, email: EmailStr, password_hash: str):
        users = self.load_users()
        users[email] = {"email": email, "password_hash": password_hash}
        self.save_users(users)

    def user_exists(self, email: EmailStr) -> bool:
        users = self.load_users()
        return email in users

user_db = UserDB()
