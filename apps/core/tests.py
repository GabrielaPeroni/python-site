from django.test import Client, TestCase
from django.urls import reverse

from apps.accounts.models import User
from apps.explore.models import Category, Place


class LandingPageTests(TestCase):
    """Teste suite pra funcionalidade da pagina inicial"""

    def setUp(self):
        """Prepara a data"""
        self.client = Client()
        self.url = reverse("core:landing")

        # Cria as categorias de teste
        self.category1 = Category.objects.create(
            name="Restaurantes", slug="restaurantes", icon="🍽️"
        )
        self.category2 = Category.objects.create(
            name="Natureza", slug="natureza", icon="🌳"
        )

    def test_landing_page_loads(self):
        """Testa que a pagina inicial carrega"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/landing.html")

    def test_landing_page_shows_categories(self):
        """Testa que a pagina inicial mostra categorias"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Restaurantes")
        self.assertContains(response, "Natureza")
        self.assertContains(response, "🍽️")
        self.assertContains(response, "🌳")

    def test_landing_page_shows_title(self):
        """Testa que a pagina inicial mostra o titulo correto"""
        response = self.client.get(self.url)
        self.assertContains(response, "MaricaCity")
        self.assertContains(response, "Descubra")

    def test_landing_page_has_cta_buttons(self):
        """Test that landing page has call-to-action buttons"""
        response = self.client.get(self.url)
        self.assertContains(response, "Explorar")
        self.assertContains(response, "Cadastre-se")

    def test_landing_page_shows_hero_section(self):
        """Testa que a pagina inicial tem o carrosel"""
        response = self.client.get(self.url)
        self.assertContains(response, "hero-section")
        self.assertContains(response, "swiper")

    def test_landing_page_shows_google_maps_section(self):
        """Testa que a pagina inicial tem o google-maps"""
        response = self.client.get(self.url)
        self.assertContains(response, "landing-map")
        self.assertContains(response, "Navegue pelos Lugares")


class AboutPageTests(TestCase):
    """Teste suite pra funcionalidade da pagina Sobre"""

    def setUp(self):
        """Prepara a data"""
        self.client = Client()
        self.url = reverse("core:about")

    def test_about_page_loads(self):
        """Testa que a pagina Sobre carrega"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/about.html")

    def test_about_page_contains_info(self):
        """Testa que a pagina Sobre contem informacoes"""
        response = self.client.get(self.url)
        self.assertContains(response, "Sobre")


class AdminDashboardTests(TestCase):
    """Teste suite pra funcionalidade do admin dashboard"""

    def setUp(self):
        """Prepara a data"""
        self.client = Client()
        self.url = reverse("core:admin_dashboard")

        self.staff_user = User.objects.create_user(
            username="staffuser", password="testpass123", is_staff=True
        )
        self.regular_user = User.objects.create_user(
            username="regularuser", password="testpass123", is_staff=False
        )

        self.category = Category.objects.create(
            name="Restaurantes", slug="restaurantes", icon="🍽️"
        )

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
        """Testa que o admin dash requer autenticacao"""
        response = self.client.get(self.url)
        self.assertRedirects(response, f"/?next={self.url}")

    def test_admin_dashboard_requires_staff_permission(self):
        """Testa que o admin dash requer permissao de staff (is_staff=True)"""
        # Try with regular user - should be denied access
        self.client.login(username="regularuser", password="testpass123")
        response = self.client.get(self.url)
        # Should either return 403 or redirect (both are valid)
        self.assertIn(response.status_code, [302, 403])

    def test_admin_dashboard_loads_for_staff(self):
        """Testa que o admin dash carrega para staff"""
        self.client.login(username="staffuser", password="testpass123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/admin_dashboard.html")

    def test_admin_dashboard_shows_statistics(self):
        """Testa que o that admin dash mostra statisticas"""
        self.client.login(username="staffuser", password="testpass123")
        response = self.client.get(self.url)

        self.assertIn("total_places", response.context)
        self.assertIn("pending_places", response.context)
        self.assertIn("approved_places", response.context)
        self.assertIn("total_users", response.context)

        self.assertEqual(response.context["total_places"], 2)
        self.assertEqual(response.context["pending_places"], 1)
        self.assertEqual(response.context["approved_places"], 1)
        self.assertEqual(response.context["total_users"], 2)

    def test_admin_dashboard_shows_content(self):
        """Testa que o that admin dash mostra conteudo relevante"""
        self.client.login(username="staffuser", password="testpass123")
        response = self.client.get(self.url)

        self.assertContains(response, "Dashboard")
