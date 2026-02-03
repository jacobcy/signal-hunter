import json
import os
from enum import Enum
from typing import Dict, List, Optional, Any

class UserRole(Enum):
    OWNER = "OWNER"
    CONTRIBUTOR = "CONTRIBUTOR"
    SUBSCRIBER = "SUBSCRIBER"

# Define permission mappings
PERMISSIONS = {
    UserRole.OWNER.value: ["*"],
    UserRole.CONTRIBUTOR.value: ["report", "feature"],
    UserRole.SUBSCRIBER.value: ["read"]
}

DEFAULT_ROLE = UserRole.SUBSCRIBER.value
USERS_FILE = "memory/users.json"

class UserManager:
    def __init__(self, users_file: str = USERS_FILE):
        self.users_file = users_file
        self.users: Dict[str, Dict[str, Any]] = {}
        self.load_users()

    def load_users(self) -> None:
        """Loads users from the JSON file. Creates the file if it doesn't exist."""
        if not os.path.exists(self.users_file):
            # Ensure directory exists
            os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
            self.users = {}
            self.save_users()
            return

        try:
            with open(self.users_file, 'r', encoding='utf-8') as f:
                self.users = json.load(f)
        except (json.JSONDecodeError, IOError) as e:
            print(f"Error loading users from {self.users_file}: {e}")
            self.users = {}

    def save_users(self) -> None:
        """Saves the current users dictionary to the JSON file."""
        try:
            # Ensure directory exists before saving (in case it was deleted)
            os.makedirs(os.path.dirname(self.users_file), exist_ok=True)
            with open(self.users_file, 'w', encoding='utf-8') as f:
                json.dump(self.users, f, indent=4, ensure_ascii=False)
        except IOError as e:
            print(f"Error saving users to {self.users_file}: {e}")

    def get_user(self, user_id: str) -> Optional[Dict[str, Any]]:
        """Retrieves a user by ID."""
        return self.users.get(str(user_id))

    def create_user(self, user_id: str, role: str = DEFAULT_ROLE) -> Dict[str, Any]:
        """Creates a new user or returns the existing one."""
        user_id = str(user_id)
        if user_id in self.users:
            return self.users[user_id]
        
        if role not in PERMISSIONS:
            role = DEFAULT_ROLE
            
        new_user = {
            "id": user_id,
            "role": role,
            "created_at": "TODO: Add timestamp if needed" 
        }
        self.users[user_id] = new_user
        self.save_users()
        return new_user

    def check_permission(self, user_id: str, action: str) -> bool:
        """
        Checks if a user has permission to perform an action.
        Returns False if user does not exist.
        """
        user = self.get_user(user_id)
        if not user:
            return False
        
        role = user.get("role", DEFAULT_ROLE)
        allowed_actions = PERMISSIONS.get(role, [])
        
        if "*" in allowed_actions:
            return True
            
        return action in allowed_actions
