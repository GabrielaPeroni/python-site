from datetime import timedelta

from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.accounts.models import User
from apps.news.models import News, NewsCategory


class Command(BaseCommand):
    help = "Seed the database with sample news and events"

    def handle(self, *args, **options):
        self.stdout.write("Seeding news categories...")

        # Create categories
        news_cat, _ = NewsCategory.objects.get_or_create(
            name=NewsCategory.NEWS,
            defaults={"description": "General news about Maricá", "icon": "📰"},
        )

        event_cat, _ = NewsCategory.objects.get_or_create(
            name=NewsCategory.EVENT,
            defaults={"description": "Events happening in Maricá", "icon": "📅"},
        )

        announcement_cat, _ = NewsCategory.objects.get_or_create(
            name=NewsCategory.ANNOUNCEMENT,
            defaults={"description": "Official announcements", "icon": "📢"},
        )

        self.stdout.write(self.style.SUCCESS("Categories created"))

        # Get or create a staff user for authorship
        admin_user = User.objects.filter(is_staff=True).first()
        if not admin_user:
            admin_user = User.objects.first()

        if not admin_user:
            self.stdout.write(
                self.style.ERROR("No users found. Please create a user first.")
            )
            return

        self.stdout.write(f"Using author: {admin_user.username}")

        # Create sample news
        news_items = [
            {
                "title": "Nova Praia de Maricá Inaugurada",
                "content": """A Prefeitura de Maricá inaugurou hoje uma nova área de praia na região leste da cidade. O local conta com infraestrutura completa, incluindo quiosques, estacionamento e salva-vidas.

A nova praia promete se tornar um dos principais pontos turísticos da cidade, com suas águas cristalinas e areia branca. O prefeito destacou que o investimento faz parte do projeto de valorização do turismo local.

Os visitantes poderão desfrutar de toda a infraestrutura desde este final de semana.""",
                "category": news_cat,
                "is_featured": True,
                "publish_date": timezone.now() - timedelta(days=2),
            },
            {
                "title": "Festival de Música na Praça Central",
                "content": """O tradicional Festival de Música de Maricá acontecerá no próximo sábado na Praça Central. O evento contará com apresentações de artistas locais e nacionais, prometendo uma noite inesquecível.

A programação inclui shows de MPB, samba, rock e música eletrônica. A entrada é gratuita e haverá food trucks e barracas de artesanato local.

O festival começa às 16h e vai até meia-noite. Traga sua família e amigos para aproveitar!""",
                "category": event_cat,
                "event_date": timezone.now() + timedelta(days=7),
                "event_location": "Praça Central de Maricá",
                "is_featured": True,
                "publish_date": timezone.now() - timedelta(days=5),
            },
            {
                "title": "Manutenção Programada na Rede de Água",
                "content": """A Companhia de Águas de Maricá informa que haverá manutenção programada na rede de abastecimento na próxima terça-feira, das 8h às 14h.

Os bairros afetados serão: Centro, São José e Jardim Atlântico. Recomenda-se que os moradores armazenem água com antecedência.

A empresa pede desculpas pelo transtorno e agradece a compreensão.""",
                "category": announcement_cat,
                "publish_date": timezone.now() - timedelta(days=1),
            },
            {
                "title": "Curso Gratuito de Artesanato",
                "content": """A Secretaria de Cultura oferece curso gratuito de artesanato a partir da próxima segunda-feira. As aulas acontecerão no Centro Cultural, sempre às terças e quintas-feiras, das 14h às 17h.

O curso tem duração de 3 meses e ensina técnicas de crochê, tricô, macramê e bordado. As vagas são limitadas e as inscrições devem ser feitas presencialmente no Centro Cultural.

Material básico será fornecido pela prefeitura. Certificado ao final do curso.""",
                "category": event_cat,
                "event_date": timezone.now() + timedelta(days=10),
                "event_location": "Centro Cultural de Maricá",
                "publish_date": timezone.now() - timedelta(days=3),
            },
            {
                "title": "MaricaCity Atinge 10 Mil Usuários",
                "content": """A plataforma MaricaCity comemora a marca de 10 mil usuários cadastrados! Lançada há apenas 6 meses, a plataforma se tornou a principal ferramenta para descobrir pontos turísticos e serviços na cidade.

Agradecemos a todos os usuários que contribuíram com avaliações, fotos e sugestões de lugares. Continuaremos trabalhando para melhorar ainda mais a experiência de todos.

Novas funcionalidades estão a caminho!""",
                "category": news_cat,
                "is_featured": True,
                "publish_date": timezone.now() - timedelta(hours=12),
            },
            {
                "title": "Feira de Orgânicos Todo Domingo",
                "content": """A Feira de Produtos Orgânicos acontece todos os domingos na Praça da Matriz, das 7h às 13h. Produtos frescos direto do produtor, sem agrotóxicos.

Você encontra frutas, verduras, legumes, ovos caipiras, mel, pães artesanais e muito mais. Venha apoiar a agricultura local e se alimentar de forma mais saudável!

Aceitamos dinheiro e cartão.""",
                "category": event_cat,
                "event_date": timezone.now() + timedelta(days=3),
                "event_location": "Praça da Matriz",
                "publish_date": timezone.now() - timedelta(days=7),
            },
        ]

        created_count = 0
        for news_data in news_items:
            news_data["author"] = admin_user
            news_data["status"] = News.PUBLISHED
            news, created = News.objects.get_or_create(
                title=news_data["title"], defaults=news_data
            )
            if created:
                created_count += 1
                self.stdout.write(f"  Created: {news.title}")

        self.stdout.write(
            self.style.SUCCESS(f"\n{created_count} news items created successfully!")
        )
