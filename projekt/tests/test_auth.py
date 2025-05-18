import unittest

from src.auth import Auth
from src.user import User, UserRole


class TestAuth(unittest.TestCase):
    """Test cases for the Auth class."""

    def setUp(self):
        """Set up test fixtures."""
        self.auth = Auth()

        self.user = User(
            id=1,
            name="John",
            last_name="Doe",
            email="john@example.com",
            password="Password123!",
            phone="523456789",
        )

        self.admin = User(
            id=2,
            name="Admin",
            last_name="User",
            email="admin@example.com",
            password="Admin123!",
            phone="789456123",
            role=UserRole.ADMIN,
        )

    def test_login_success(self):
        """Test successful login with valid credentials."""

        result = self.auth.login(
            user=self.user, email="john@example.com", password="Password123!"
        )

        self.assertTrue(result)
        self.assertIn(self.user.id, self.auth.logged_users)
        self.assertEqual(self.auth.logged_users[self.user.id], self.user)

    def test_login_invalid_email_type(self):
        """Test login with invalid email type."""

        with self.assertRaises(TypeError):
            self.auth.login(user=self.user, email=123, password="Password123!")

    def test_login_invalid_password_type(self):
        """Test login with invalid password type."""

        with self.assertRaises(TypeError):
            self.auth.login(user=self.user, email="john@example.com", password=123)

    def test_login_invalid_credentials(self):
        """Test login with invalid credentials."""

        with self.assertRaises(PermissionError):
            self.auth.login(
                user=self.user, email="wrong@example.com", password="Password123!"
            )

        with self.assertRaises(PermissionError):
            self.auth.login(
                user=self.user, email="john@example.com", password="WrongPassword123!"
            )

    def test_login_already_logged_in(self):
        """Test login when user is already logged in."""

        self.auth.login(
            user=self.user, email="john@example.com", password="Password123!"
        )

        with self.assertRaises(PermissionError):
            self.auth.login(
                user=self.user, email="john@example.com", password="Password123!"
            )

    def test_logout_success(self):
        """Test successful logout."""

        self.auth.login(
            user=self.user, email="john@example.com", password="Password123!"
        )

        result = self.auth.logout(user=self.user)

        self.assertTrue(result)
        self.assertNotIn(self.user.id, self.auth.logged_users)

    def test_logout_not_logged_in(self):
        """Test logout when user is not logged in."""
        with self.assertRaises(PermissionError):
            self.auth.logout(user=self.user)

    def test_is_logged_in(self):
        """Test checking if user is logged in."""

        initial_status = self.auth.is_logged_in(user=self.user)
        self.assertFalse(initial_status)

        self.auth.login(
            user=self.user, email="john@example.com", password="Password123!"
        )
        logged_in_status = self.auth.is_logged_in(user=self.user)
        self.assertTrue(logged_in_status)

        self.auth.logout(user=self.user)
        final_status = self.auth.is_logged_in(user=self.user)
        self.assertFalse(final_status)

    def test_is_admin(self):
        """Test checking if user is an admin."""
        user_admin_status = self.auth.is_admin(user=self.user)
        admin_admin_status = self.auth.is_admin(user=self.admin)

        self.assertFalse(user_admin_status)
        self.assertTrue(admin_admin_status)

    def test_login_logout_multiple_users(self):
        """Test login and logout with multiple users."""

        self.auth.login(
            user=self.user, email="john@example.com", password="Password123!"
        )
        self.auth.login(
            user=self.admin, email="admin@example.com", password="Admin123!"
        )

        user_logged_in = self.auth.is_logged_in(user=self.user)
        admin_logged_in = self.auth.is_logged_in(user=self.admin)

        self.assertTrue(user_logged_in)
        self.assertTrue(admin_logged_in)

        self.auth.logout(user=self.user)

        user_logged_in_after_logout = self.auth.is_logged_in(user=self.user)
        admin_logged_in_after_user_logout = self.auth.is_logged_in(user=self.admin)

        self.assertFalse(user_logged_in_after_logout)
        self.assertTrue(admin_logged_in_after_user_logout)

    if __name__ == "__main__":
        unittest.main()
