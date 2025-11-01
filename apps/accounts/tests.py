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
        )
        self.assertEqual(user.username, "testuser")
        self.assertEqual(user.email, "test@example.com")
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
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_user_string_representation(self):
        """Test the string representation of user"""
        user = User.objects.create_user(username="testuser", password="pass123")
        self.assertEqual(str(user), "testuser")

    def test_user_permissions_properties(self):
        """Test custom permission properties"""
        regular_user = User.objects.create_user(
            username="regular", password="pass123", is_staff=False
        )
        staff_user = User.objects.create_user(
            username="staff", password="pass123", is_staff=True
        )

        # Test can_create_places - all authenticated users can create
        self.assertTrue(regular_user.can_create_places)
        self.assertTrue(staff_user.can_create_places)

        # Test can_moderate - only staff users can moderate
        self.assertFalse(regular_user.can_moderate)
        self.assertTrue(staff_user.can_moderate)

    def test_all_logged_in_users_can_create_places(self):
        """Test that all logged-in users can create places"""
        regular_user = User.objects.create_user(
            username="regular", password="pass123", is_staff=False
        )
        self.assertTrue(regular_user.can_create_places)

    def test_only_staff_can_moderate(self):
        """Test that only staff users can moderate"""
        regular_user = User.objects.create_user(
            username="regular", password="pass123", is_staff=False
        )
        staff_user = User.objects.create_user(
            username="staff", password="pass123", is_staff=True
        )
        self.assertFalse(regular_user.can_moderate)
        self.assertTrue(staff_user.can_moderate)


class AuthenticationViewTests(TestCase):
    """Tests for authentication views"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
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
                "password1": "newpass123!",
                "password2": "newpass123!",
            },
        )
        self.assertEqual(response.status_code, 302)  # Redirect after registration

        # Verify user was created
        self.assertTrue(User.objects.filter(username="newuser").exists())
        new_user = User.objects.get(username="newuser")
        self.assertEqual(new_user.email, "new@example.com")
        self.assertFalse(new_user.is_staff)  # Regular user by default

    def test_registration_form_no_user_type_field(self):
        """Test that registration form does not show user type selection"""
        response = self.client.get(reverse("accounts:register"))
        self.assertEqual(response.status_code, 200)
        # User type field should not be in the form
        self.assertNotContains(response, 'name="user_type"')

    def test_new_users_default_to_regular_account(self):
        """Test that newly registered users are regular accounts (not staff)"""
        response = self.client.post(
            reverse("accounts:register"),
            {
                "username": "newuser",
                "email": "new@example.com",
                "password1": "newpass123!",
                "password2": "newpass123!",
            },
        )
        self.assertEqual(response.status_code, 302)
        new_user = User.objects.get(username="newuser")
        self.assertFalse(new_user.is_staff)
        self.assertTrue(new_user.can_create_places)
        self.assertFalse(new_user.can_moderate)

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

    def test_quick_login_form_submission(self):
        """Test quick login via modal form"""
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "testuser", "password": "testpass123"},
            HTTP_REFERER="/explore/",
        )
        self.assertEqual(response.status_code, 302)
        # Verify user is logged in
        user = response.wsgi_request.user
        self.assertTrue(user.is_authenticated)
        self.assertEqual(user.username, "testuser")

    def test_quick_login_form_with_invalid_credentials(self):
        """Test quick login with invalid credentials"""
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "testuser", "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 200)
        # User should not be logged in
        user = response.wsgi_request.user
        self.assertFalse(user.is_authenticated)

    def test_login_dropdown_present_on_pages(self):
        """Test that login dropdown HTML is present on pages"""
        # Test on landing page
        response = self.client.get(reverse("core:landing"))
        self.assertContains(response, 'id="loginDropdown"')
        self.assertContains(response, "Entre na sua conta")

        # Test on explore page - uses includes/navbar.html
        response = self.client.get(reverse("explore:explore"))
        self.assertContains(response, "Entre na sua conta")

    def test_login_button_present_for_anonymous_users(self):
        """Test login button appears for anonymous users"""
        response = self.client.get(reverse("core:landing"))
        self.assertContains(response, 'data-bs-toggle="dropdown"')
        self.assertContains(response, "Entrar")

    def test_login_button_not_present_for_authenticated_users(self):
        """Test login button doesn't appear for authenticated users"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("core:landing"))
        # Should show Sair instead of Entrar in the dropdown
        self.assertContains(response, "Sair")
        # Should not show the login dropdown trigger
        self.assertNotContains(response, 'id="loginDropdown"')
        # Should show username
        self.assertContains(response, "testuser")

    def test_google_client_id_in_context(self):
        """Test that Google OAuth client ID is passed to login page"""
        response = self.client.get(reverse("accounts:login"))
        self.assertIn("google_client_id", response.context)

    def test_google_client_id_in_register_context(self):
        """Test that Google OAuth client ID is passed to register page"""
        response = self.client.get(reverse("accounts:register"))
        self.assertIn("google_client_id", response.context)
