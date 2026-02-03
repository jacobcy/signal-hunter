import pytest
import tempfile
import os
from src.auth.user_manager import UserManager


class TestUserManager:
    """Test suite for the User Management System."""

    def test_create_new_user(self):
        """Verify default role is SUBSCRIBER when creating a new user."""
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = os.path.join(temp_dir, "users.json")
            user_manager = UserManager(db_path)
            
            # Create a new user without specifying a role
            user_id = "test_user_123"
            user = user_manager.create_user(user_id)
            
            # Verify the user exists and has the default SUBSCRIBER role
            assert user is not None
            assert user["role"] == "SUBSCRIBER"

    def test_persistence(self):
        """Save a user, reload UserManager, verify user exists."""
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = os.path.join(temp_dir, "users.json")
            
            # Create a user manager and add a user
            user_manager1 = UserManager(db_path)
            user_id = "persistent_user_456"
            user_manager1.create_user(user_id, "OWNER")
            
            # Create a new user manager instance pointing to the same file
            user_manager2 = UserManager(db_path)
            
            # Verify the user exists in the new instance
            user = user_manager2.get_user(user_id)
            assert user is not None
            assert user["role"] == "OWNER"

    def test_permission_denial(self):
        """Verify a SUBSCRIBER cannot do OWNER actions."""
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = os.path.join(temp_dir, "users.json")
            user_manager = UserManager(db_path)
            
            # Create a subscriber user
            subscriber_id = "subscriber_789"
            user_manager.create_user(subscriber_id, "SUBSCRIBER")
            
            # Check that subscriber cannot perform 'admin' action
            assert user_manager.check_permission(subscriber_id, "admin") == False

    def test_permission_grant(self):
        """Verify OWNER can do everything."""
        with tempfile.TemporaryDirectory() as temp_dir:
            db_path = os.path.join(temp_dir, "users.json")
            user_manager = UserManager(db_path)
            
            # Create an owner user
            owner_id = "owner_101"
            user_manager.create_user(owner_id, "OWNER")
            
            # Check that owner can perform any action
            assert user_manager.check_permission(owner_id, "read") == True
            assert user_manager.check_permission(owner_id, "report") == True
            assert user_manager.check_permission(owner_id, "admin") == True