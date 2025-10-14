from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class UserModelTests(TestCase):
    """Tests for the custom User model"""

    def test_create_user(self):
        """Test creating a regular user"""
        user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            user_type="EXPLORE",
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
        self.assertEqual(user.user_type, "EXPLORE")
        self.assertTrue(user.check_password("testpass123"))
        self.assertTrue(user.is_active)
        self.assertFalse(user.is_staff)
        self.assertFalse(user.is_superuser)

    def test_create_superuser(self):
        """Test creating a superuser"""
        admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123",
            user_type="ADMIN",
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)
        self.assertEqual(admin.user_type, "ADMIN")

    def test_user_type_choices(self):
        """Test all user type choices"""
        explore_user = User.objects.create_user(
            username="explorer", password="pass123", user_type="EXPLORE"
        )
        self.assertEqual(explore_user.user_type, "EXPLORE")

        creation_user = User.objects.create_user(
            username="creator", password="pass123", user_type="CREATION"
        )
        self.assertEqual(creation_user.user_type, "CREATION")

        admin_user = User.objects.create_user(
            username="adminuser", password="pass123", user_type="ADMIN"
        )
        self.assertEqual(admin_user.user_type, "ADMIN")

    def test_user_string_representation(self):
        """Test the string representation of user"""
        user = User.objects.create_user(
            username="testuser", password="pass123", user_type="EXPLORE"
        )
        self.assertEqual(str(user), "testuser (Explore User)")

    def test_user_permissions_properties(self):
        """Test custom permission properties"""
        explore_user = User.objects.create_user(
            username="explorer", password="pass123", user_type="EXPLORE"
        )
        creation_user = User.objects.create_user(
            username="creator", password="pass123", user_type="CREATION"
        )
        admin_user = User.objects.create_user(
            username="admin", password="pass123", user_type="ADMIN"
        )

        # Test can_create_places
        self.assertFalse(explore_user.can_create_places)
        self.assertTrue(creation_user.can_create_places)
        self.assertTrue(admin_user.can_create_places)

        # Test can_moderate
        self.assertFalse(explore_user.can_moderate)
        self.assertFalse(creation_user.can_moderate)
        self.assertTrue(admin_user.can_moderate)


class AuthenticationViewTests(TestCase):
    """Tests for authentication views"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
            user_type="EXPLORE",
        )

    def test_login_page_loads(self):
        """Test login page loads successfully"""
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/login.html")

    def test_register_page_loads(self):
        """Test registration page loads successfully"""
        response = self.client.get(reverse("accounts:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_user_can_login(self):
        """Test user can login with correct credentials"""
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "testuser", "password": "testpass123"},
        )
        self.assertEqual(response.status_code, 302)  # Redirect after login

    def test_user_cannot_login_with_wrong_password(self):
        """Test user cannot login with wrong password"""
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "testuser", "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 200)  # Stay on login page

    def test_user_registration(self):
        """Test new user can register"""
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "newuser",
                "email": "new@example.com",
                "user_type": "CREATION",
                "password1": "newpass123!",
                "password2": "newpass123!",
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirect after registration

        # Verify user was created
        self.assertTrue(User.objects.filter(username="newuser").exists())
        new_user = User.objects.get(username="newuser")
        self.assertEqual(new_user.email, "new@example.com")
        self.assertEqual(new_user.user_type, "CREATION")

    def test_logout(self):
        """Test user can logout"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("accounts:logout"))
        self.assertEqual(response.status_code, 302)

    def test_authenticated_user_redirected_from_login(self):
        """Test authenticated users are redirected from login page"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 302)
