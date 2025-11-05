from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

User = get_user_model()


class UserModelTests(TestCase):
    """Testes para o modelo User personalizado"""

    def test_create_user(self):
        """Testa a criação de um usuário regular"""
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
        """Testa a criação de um superusuário"""
        admin = User.objects.create_superuser(
            username="admin",
            email="admin@example.com",
            password="admin123",
        )
        self.assertTrue(admin.is_staff)
        self.assertTrue(admin.is_superuser)

    def test_user_string_representation(self):
        """Testa a representação em string do usuário"""
        user = User.objects.create_user(username="testuser", password="pass123")
        self.assertEqual(str(user), "testuser")

    def test_user_permissions_properties(self):
        """Testa propriedades de permissões personalizadas"""
        regular_user = User.objects.create_user(
            username="regular", password="pass123", is_staff=False
        )
        staff_user = User.objects.create_user(
            username="staff", password="pass123", is_staff=True
        )

        # Testa can_create_places - todos os usuários autenticados podem criar
        self.assertTrue(regular_user.can_create_places)
        self.assertTrue(staff_user.can_create_places)

        # Testa can_moderate - apenas usuários staff podem moderar
        self.assertFalse(regular_user.can_moderate)
        self.assertTrue(staff_user.can_moderate)

    def test_all_logged_in_users_can_create_places(self):
        """Testa que todos os usuários logados podem criar lugares"""
        regular_user = User.objects.create_user(
            username="regular", password="pass123", is_staff=False
        )
        self.assertTrue(regular_user.can_create_places)

    def test_only_staff_can_moderate(self):
        """Testa que apenas usuários staff podem moderar"""
        regular_user = User.objects.create_user(
            username="regular", password="pass123", is_staff=False
        )
        staff_user = User.objects.create_user(
            username="staff", password="pass123", is_staff=True
        )
        self.assertFalse(regular_user.can_moderate)
        self.assertTrue(staff_user.can_moderate)


class AuthenticationViewTests(TestCase):
    """Testes para views de autenticação"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="testuser",
            email="test@example.com",
            password="testpass123",
        )

    def test_register_page_loads(self):
        """Testa que a página de registro carrega com sucesso"""
        response = self.client.get(reverse("accounts:register"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "accounts/register.html")

    def test_user_can_login(self):
        """Testa que o usuário pode fazer login com credenciais corretas via AJAX"""
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "testuser", "password": "testpass123"},
        )
        self.assertEqual(response.status_code, 200)  # JSON response
        data = response.json()
        self.assertTrue(data["success"])
        self.assertEqual(data["username"], "testuser")

    def test_user_cannot_login_with_wrong_password(self):
        """Testa que o usuário não pode fazer login com senha incorreta via AJAX"""
        response = self.client.post(
            reverse("accounts:login"),
            {"username": "testuser", "password": "wrongpassword"},
        )
        self.assertEqual(response.status_code, 401)  # Unauthorized
        data = response.json()
        self.assertFalse(data["success"])
        self.assertIn("error", data)

    def test_user_registration(self):
        """Testa que um novo usuário pode se registrar"""
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

        # Verificar que o usuário foi criado
        self.assertTrue(User.objects.filter(username="newuser").exists())
        new_user = User.objects.get(username="newuser")
        self.assertEqual(new_user.email, "new@example.com")
        self.assertFalse(new_user.is_staff)  # Usuário regular por padrão

    def test_registration_form_no_user_type_field(self):
        """Testa que o formulário de registro não mostra seleção de tipo de usuário"""
        response = self.client.get(reverse("accounts:register"))
        self.assertEqual(response.status_code, 200)
        # Campo de tipo de usuário não deve estar no formulário
        self.assertNotContains(response, 'name="user_type"')

    def test_new_users_default_to_regular_account(self):
        """Testa que usuários recém-registrados são contas regulares (não staff)"""
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
        """Testa que o usuário pode fazer logout"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("accounts:logout"))
        self.assertEqual(response.status_code, 302)

    def test_login_endpoint_rejects_get_requests(self):
        """Testa que o endpoint de login só aceita POST (apenas AJAX)"""
        response = self.client.get(reverse("accounts:login"))
        self.assertEqual(response.status_code, 405)  # Method not allowed
        data = response.json()
        self.assertFalse(data["success"])

    def test_login_dropdown_present_on_pages(self):
        """Testa que o dropdown de login está presente nas páginas"""
        # Testar na página inicial
        response = self.client.get(reverse("core:landing"))
        self.assertContains(response, "Entre na sua conta")
        self.assertContains(response, 'data-bs-toggle="dropdown"')

        # Testar na página de explorar
        response = self.client.get(reverse("explore:explore"))
        self.assertContains(response, "Entre na sua conta")
        self.assertContains(response, 'data-bs-toggle="dropdown"')

    def test_login_button_present_for_anonymous_users(self):
        """Testa que o botão de login aparece para usuários anônimos"""
        response = self.client.get(reverse("core:landing"))
        self.assertContains(response, 'data-bs-toggle="dropdown"')
        self.assertContains(response, "Entrar")

    def test_login_button_not_present_for_authenticated_users(self):
        """Testa que o botão de login não aparece para usuários autenticados"""
        self.client.login(username="testuser", password="testpass123")
        response = self.client.get(reverse("core:landing"))
        # Deve mostrar Sair em vez de Entrar
        self.assertContains(response, "Sair")
        # Deve mostrar o nome de usuário
        self.assertContains(response, "testuser")

    def test_google_client_id_in_register_context(self):
        """Testa que o ID do cliente Google OAuth é passado para a página de registro"""
        response = self.client.get(reverse("accounts:register"))
        self.assertIn("google_client_id", response.context)
