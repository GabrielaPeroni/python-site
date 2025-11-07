from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.accounts.models import User
from apps.explore.models import Category, Place, PlaceApproval


class Command(BaseCommand):
    help = "Preencher banco de dados com dados de teste para desenvolvimento"

    def handle(self, *args, **options):
        self.stdout.write("Criando dados de teste...")

        # Obter usuários existentes
        self.stdout.write("Obtendo usuários...")

        # Usuário administrador (deve existir)
        admin = User.objects.filter(username="admin").first()
        if not admin:
            self.stdout.write(
                self.style.ERROR("Admin user not found. Please create it first.")
            )
            return

        # Usuário normal (deve existir)
        normal_user = User.objects.filter(username="user").first()
        if not normal_user:
            self.stdout.write(
                self.style.ERROR("Normal user not found. Please create it first.")
            )
            return

        # Criar categorias
        self.stdout.write("Criando categorias...")
        categories_data = [
            {
                "name": "Restaurantes",
                "slug": "restaurantes",
                "icon": "🍽️",
                "description": "Melhores lugares para comer em Maricá",
                "display_order": 1,
            },
            {
                "name": "Hotéis e Pousadas",
                "slug": "hoteis-pousadas",
                "icon": "🏨",
                "description": "Acomodações confortáveis",
                "display_order": 2,
            },
            {
                "name": "Natureza e Parques",
                "slug": "natureza-parques",
                "icon": "🌳",
                "description": "Áreas naturais e parques",
                "display_order": 3,
            },
            {
                "name": "Artes e Cultura",
                "slug": "artes-cultura",
                "icon": "🎨",
                "description": "Atrações culturais e museus",
                "display_order": 4,
            },
            {
                "name": "Praias",
                "slug": "praias",
                "icon": "🏖️",
                "description": "Praias deslumbrantes e pontos costeiros",
                "display_order": 5,
            },
            {
                "name": "Compras",
                "slug": "compras",
                "icon": "🛍️",
                "description": "Lojas locais e mercados",
                "display_order": 6,
            },
        ]

        categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=cat_data["slug"], defaults=cat_data
            )
            categories[cat_data["slug"]] = cat
            if created:
                self.stdout.write(self.style.SUCCESS(f"Created category: {cat.name}"))

        # Criar lugares
        self.stdout.write("Criando lugares...")
        places_data = [
            # Lugares aprovados
            {
                "name": "Praia de Maricá",
                "description": "Linda praia com águas cristalinas e areia dourada. Perfeita para natação e esportes aquáticos.",
                "address": "Avenida Litorânea, Maricá, RJ",
                "categories": ["praias", "natureza-parques"],
                "is_approved": True,
                "created_days_ago": 5,
            },
            {
                "name": "Restaurante Mar e Sol",
                "description": "Restaurante tradicional de frutos do mar com vista incrível para o oceano. Especializado em peixes frescos e culinária local.",
                "address": "Rua das Praias, 123, Centro, Maricá, RJ",
                "categories": ["restaurantes"],
                "is_approved": True,
                "created_days_ago": 10,
            },
            {
                "name": "Lagoa de Araçatiba",
                "description": "Linda lagoa perfeita para caiaque, stand-up paddle e relaxamento. Cercada pela natureza.",
                "address": "Araçatiba, Maricá, RJ",
                "categories": ["natureza-parques", "praias"],
                "is_approved": True,
                "created_days_ago": 15,
            },
            # Lugar pendente de aprovação
            {
                "name": "Pousada Vida Boa",
                "description": "Pousada aconchegante com atendimento personalizado e café da manhã caseiro. Perto das principais atrações.",
                "address": "Rua Tranquila, 25, Maricá, RJ",
                "categories": ["hoteis-pousadas"],
                "is_approved": False,
                "created_days_ago": 1,
            },
        ]

        for place_data in places_data:
            # Extrair categorias
            cat_slugs = place_data.pop("categories")
            created_days_ago = place_data.pop("created_days_ago", 0)

            # Criar lugar
            place, created = Place.objects.get_or_create(
                name=place_data["name"],
                defaults={
                    **place_data,
                    "created_by": normal_user,
                },
            )

            if created:
                # Definir created_at para simular datas diferentes
                place.created_at = timezone.now() - timedelta(days=created_days_ago)
                place.save()

                # Adicionar categorias
                for slug in cat_slugs:
                    if slug in categories:
                        place.categories.add(categories[slug])

                # Criar registro de aprovação se aprovado
                if place.is_approved:
                    PlaceApproval.objects.create(
                        place=place,
                        reviewer=admin,
                        action="APPROVE",
                        comments="Aprovado durante criação de dados de teste",
                    )

                self.stdout.write(self.style.SUCCESS(f"Created place: {place.name}"))

        # Resumo
        self.stdout.write(self.style.SUCCESS("\n=== Test Data Summary ==="))
        self.stdout.write(f"Users: {User.objects.count()}")
        self.stdout.write(f"Categories: {Category.objects.count()}")
        self.stdout.write(f"Places (Total): {Place.objects.count()}")
        self.stdout.write(
            f"Places (Approved): {Place.objects.filter(is_approved=True).count()}"
        )
        self.stdout.write(
            f"Places (Pending): {Place.objects.filter(is_approved=False).count()}"
        )

        self.stdout.write(self.style.SUCCESS("\nDados de teste criados com sucesso!"))
        self.stdout.write("\nCredenciais:")
        self.stdout.write("Admin: admin / admin")
        self.stdout.write("Usuario: user / user")
