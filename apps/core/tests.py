from django.test import Client, TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.explore.models import Category, Place


class LandingPageTests(TestCase):
    """Test suite for landing page functionality"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.url = reverse("core:landing")

        # Create test categories
        self.category1 = Category.objects.create(
            name="Restaurantes", slug="restaurantes", icon="🍽️"
        )
        self.category2 = Category.objects.create(
            name="Natureza", slug="natureza", icon="🌳"
        )

    def test_landing_page_loads(self):
        """Test that landing page loads successfully"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/landing.html")

    def test_landing_page_shows_categories(self):
        """Test that landing page displays categories"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Restaurantes")
        self.assertContains(response, "Natureza")
        self.assertContains(response, "🍽️")
        self.assertContains(response, "🌳")

    def test_landing_page_shows_title(self):
        """Test that landing page shows correct title"""
        response = self.client.get(self.url)
        self.assertContains(response, "MaricaCity")
        self.assertContains(response, "Descubra")

    def test_landing_page_has_cta_buttons(self):
        """Test that landing page has call-to-action buttons"""
        response = self.client.get(self.url)
        self.assertContains(response, "Explorar")
        self.assertContains(response, "Cadastre-se")

    def test_landing_page_shows_hero_section(self):
        """Test that landing page has hero carousel section"""
        response = self.client.get(self.url)
        self.assertContains(response, "hero-section")
        self.assertContains(response, "swiper")

    def test_landing_page_shows_google_maps_section(self):
        """Test that landing page includes Google Maps section"""
        response = self.client.get(self.url)
        self.assertContains(response, "landing-map")
        self.assertContains(response, "Navegue pelos Lugares")


class AboutPageTests(TestCase):
    """Test suite for about page functionality"""

    def setUp(self):
        """Set up test client"""
        self.client = Client()
        self.url = reverse("core:about")

    def test_about_page_loads(self):
        """Test that about page loads successfully"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/about.html")

    def test_about_page_contains_info(self):
        """Test that about page contains site information"""
        response = self.client.get(self.url)
        self.assertContains(response, "Sobre")


class AdminDashboardTests(TestCase):
    """Test suite for admin dashboard functionality"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.url = reverse("core:admin_dashboard")

        # Create test users with new simplified model
        self.staff_user = User.objects.create_user(
            username="staffuser", password="testpass123", is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username="regularuser", password="testpass123", is_staff=False
        )

        # Create test category
        self.category = Category.objects.create(
            name="Restaurantes", slug="restaurantes", icon="🍽️"
        )

        # Create some test places
        self.approved_place = Place.objects.create(
            name="Approved Place",
            description="An approved place",
            address="123 Test St",
            created_by=self.regular_user,
            is_approved=True,
        )

        self.pending_place = Place.objects.create(
            name="Pending Place",
            description="A pending place",
            address="456 Test Ave",
            created_by=self.regular_user,
            is_approved=False,
        )

    def test_admin_dashboard_requires_login(self):
        """Test that admin dashboard requires authentication"""
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/?next={self.url}")

    def test_admin_dashboard_requires_staff_permission(self):
        """Test that admin dashboard requires staff permission (is_staff=True)"""
        # Try with regular user - should be denied access
        self.client.login(username="regularuser", password="testpass123")
        response = self.client.get(self.url)
        # Should either return 403 or redirect (both are valid)
        self.assertIn(response.status_code, [302, 403])

    def test_admin_dashboard_loads_for_staff(self):
        """Test that admin dashboard loads successfully for staff users"""
        self.client.login(username="staffuser", password="testpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/admin_dashboard.html")

    def test_admin_dashboard_shows_statistics(self):
        """Test that admin dashboard displays key statistics"""
        self.client.login(username="staffuser", password="testpass123")
        response = self.client.get(self.url)

        # Check for statistics in context
        self.assertIn("total_places", response.context)
        self.assertIn("pending_places", response.context)
        self.assertIn("approved_places", response.context)
        self.assertIn("total_users", response.context)

        # Verify the counts are correct
        self.assertEqual(response.context["total_places"], 2)
        self.assertEqual(response.context["pending_places"], 1)
        self.assertEqual(response.context["approved_places"], 1)
        self.assertEqual(
            response.context["total_users"], 2
        )  # staff_user and regular_user

    def test_admin_dashboard_shows_content(self):
        """Test that admin dashboard shows relevant content"""
        self.client.login(username="staffuser", password="testpass123")
        response = self.client.get(self.url)

        # Should show dashboard content
        self.assertContains(response, "Dashboard")

    def test_admin_dashboard_links_to_approval_queue(self):
        """Test that admin dashboard has link to approval queue"""
        self.client.login(username="staffuser", password="testpass123")
        response = self.client.get(self.url)
        self.assertContains(response, reverse("explore:approval_queue"))
