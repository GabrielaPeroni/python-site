from django.core.management.base import BaseCommand
from django.utils import timezone
from datetime import timedelta
from apps.accounts.models import User
from apps.explore.models import Category, Place, PlaceImage, PlaceApproval


class Command(BaseCommand):
    help = 'Populate database with test data for development'

    def handle(self, *args, **options):
        self.stdout.write('Creating test data...')

        # Create test users
        self.stdout.write('Creating users...')

        # Admin user (already created, just get it)
        admin = User.objects.filter(username='admin').first()
        if not admin:
            admin = User.objects.create_superuser(
                username='admin',
                email='admin@maricacity.com',
                password='admin123',
                user_type='ADMIN'
            )

        # Creation user
        creator, created = User.objects.get_or_create(
            username='creator1',
            defaults={
                'email': 'creator@maricacity.com',
                'user_type': 'CREATION',
                'bio': 'Local tourism enthusiast and content creator'
            }
        )
        if created:
            creator.set_password('creator123')
            creator.save()
            self.stdout.write(self.style.SUCCESS(f'Created user: {creator.username}'))

        # Explore user
        explorer, created = User.objects.get_or_create(
            username='explorer1',
            defaults={
                'email': 'explorer@maricacity.com',
                'user_type': 'EXPLORE',
                'bio': 'Loves discovering new places in Marica'
            }
        )
        if created:
            explorer.set_password('explorer123')
            explorer.save()
            self.stdout.write(self.style.SUCCESS(f'Created user: {explorer.username}'))

        # Create categories
        self.stdout.write('Creating categories...')
        categories_data = [
            {'name': 'Restaurants', 'slug': 'restaurants', 'icon': '🍽️', 'description': 'Best dining spots in Marica', 'display_order': 1},
            {'name': 'Hotels', 'slug': 'hotels', 'icon': '🏨', 'description': 'Comfortable accommodations', 'display_order': 2},
            {'name': 'Nature & Parks', 'slug': 'nature-parks', 'icon': '🌳', 'description': 'Beautiful natural areas', 'display_order': 3},
            {'name': 'Arts & Culture', 'slug': 'arts-culture', 'icon': '🎨', 'description': 'Cultural attractions and museums', 'display_order': 4},
            {'name': 'Beach', 'slug': 'beach', 'icon': '🏖️', 'description': 'Stunning beaches and coastal spots', 'display_order': 5},
            {'name': 'Shopping', 'slug': 'shopping', 'icon': '🛍️', 'description': 'Local shops and markets', 'display_order': 6},
        ]

        categories = {}
        for cat_data in categories_data:
            cat, created = Category.objects.get_or_create(
                slug=cat_data['slug'],
                defaults=cat_data
            )
            categories[cat_data['slug']] = cat
            if created:
                self.stdout.write(self.style.SUCCESS(f'Created category: {cat.name}'))

        # Create places
        self.stdout.write('Creating places...')
        places_data = [
            {
                'name': 'Praia de Marica',
                'description': 'Beautiful beach with crystal clear waters and golden sand. Perfect for swimming and water sports.',
                'address': 'Avenida Litorânea, Maricá, RJ',
                'contact_phone': '(21) 98765-4321',
                'contact_email': 'contato@praiademarica.com.br',
                'contact_website': 'https://praiademarica.com.br',
                'categories': ['beach', 'nature-parks'],
                'is_approved': True,
                'created_days_ago': 2,
            },
            {
                'name': 'Restaurante Mar e Sol',
                'description': 'Traditional seafood restaurant with amazing ocean views. Specializes in fresh fish and local cuisine.',
                'address': 'Rua das Praias, 123, Centro, Maricá, RJ',
                'contact_phone': '(21) 3333-4444',
                'contact_email': 'contato@maresol.com.br',
                'categories': ['restaurants'],
                'is_approved': True,
                'created_days_ago': 5,
            },
            {
                'name': 'Hotel Maricá Beach',
                'description': 'Comfortable beachfront hotel with modern amenities and excellent service. All rooms have ocean views.',
                'address': 'Avenida Atlântica, 456, Maricá, RJ',
                'contact_phone': '(21) 2222-3333',
                'contact_email': 'reservas@maricabeach.com',
                'contact_website': 'https://maricabeach.com',
                'categories': ['hotels'],
                'is_approved': True,
                'created_days_ago': 10,
            },
            {
                'name': 'Parque Natural Municipal',
                'description': 'Protected natural area with hiking trails, native wildlife, and stunning viewpoints.',
                'address': 'Estrada do Parque, Km 5, Maricá, RJ',
                'categories': ['nature-parks'],
                'is_approved': True,
                'created_days_ago': 15,
            },
            {
                'name': 'Galeria de Arte Maricá',
                'description': 'Contemporary art gallery featuring local and national artists. Rotating exhibitions throughout the year.',
                'address': 'Rua Cultural, 789, Centro, Maricá, RJ',
                'contact_phone': '(21) 4444-5555',
                'contact_email': 'info@galeriamarica.art',
                'categories': ['arts-culture'],
                'is_approved': True,
                'created_days_ago': 3,
            },
            {
                'name': 'Pizzaria Bella Napoli',
                'description': 'Authentic Italian pizza made in a wood-fired oven. Family-friendly atmosphere.',
                'address': 'Praça Central, 50, Maricá, RJ',
                'contact_phone': '(21) 5555-6666',
                'categories': ['restaurants'],
                'is_approved': True,
                'created_days_ago': 1,
            },
            {
                'name': 'Mercado Municipal',
                'description': 'Traditional local market with fresh produce, handicrafts, and regional products.',
                'address': 'Rua do Comércio, 100, Centro, Maricá, RJ',
                'categories': ['shopping'],
                'is_approved': True,
                'created_days_ago': 20,
            },
            {
                'name': 'Lagoa de Araçatiba',
                'description': 'Beautiful lagoon perfect for kayaking, stand-up paddle, and relaxation. Surrounded by nature.',
                'address': 'Araçatiba, Maricá, RJ',
                'categories': ['nature-parks', 'beach'],
                'is_approved': True,
                'created_days_ago': 8,
            },
            {
                'name': 'Pousada Vida Boa',
                'description': 'Cozy guesthouse with personalized service and homemade breakfast. Close to main attractions.',
                'address': 'Rua Tranquila, 25, Maricá, RJ',
                'contact_phone': '(21) 7777-8888',
                'contact_email': 'contato@pousadavidaboa.com',
                'categories': ['hotels'],
                'is_approved': True,
                'created_days_ago': 4,
            },
            {
                'name': 'Café Cultural',
                'description': 'Charming café with live music, book readings, and art exhibitions. Great coffee and pastries.',
                'address': 'Rua Boêmia, 15, Centro, Maricá, RJ',
                'contact_phone': '(21) 9999-0000',
                'categories': ['restaurants', 'arts-culture'],
                'is_approved': True,
                'created_days_ago': 6,
            },
            # Pending approval places
            {
                'name': 'Nova Praia Secreta',
                'description': 'Hidden beach recently discovered, perfect for those seeking tranquility.',
                'address': 'Acesso pela Estrada da Costa, Maricá, RJ',
                'categories': ['beach'],
                'is_approved': False,
                'created_days_ago': 1,
            },
            {
                'name': 'Restaurante em Aprovação',
                'description': 'New restaurant waiting for admin approval.',
                'address': 'Rua Nova, 999, Maricá, RJ',
                'categories': ['restaurants'],
                'is_approved': False,
                'created_days_ago': 0,
            },
        ]

        for place_data in places_data:
            # Extract categories
            cat_slugs = place_data.pop('categories')
            created_days_ago = place_data.pop('created_days_ago', 0)

            # Create place
            place, created = Place.objects.get_or_create(
                name=place_data['name'],
                defaults={
                    **place_data,
                    'created_by': creator,
                }
            )

            if created:
                # Set created_at to simulate different dates
                place.created_at = timezone.now() - timedelta(days=created_days_ago)
                place.save()

                # Add categories
                for slug in cat_slugs:
                    if slug in categories:
                        place.categories.add(categories[slug])

                # Create approval record if approved
                if place.is_approved:
                    PlaceApproval.objects.create(
                        place=place,
                        reviewer=admin,
                        action='APPROVE',
                        comments='Approved during test data creation'
                    )

                self.stdout.write(self.style.SUCCESS(f'Created place: {place.name}'))

        # Summary
        self.stdout.write(self.style.SUCCESS('\n=== Test Data Summary ==='))
        self.stdout.write(f'Users: {User.objects.count()}')
        self.stdout.write(f'Categories: {Category.objects.count()}')
        self.stdout.write(f'Places (Total): {Place.objects.count()}')
        self.stdout.write(f'Places (Approved): {Place.objects.filter(is_approved=True).count()}')
        self.stdout.write(f'Places (Pending): {Place.objects.filter(is_approved=False).count()}')

        self.stdout.write(self.style.SUCCESS('\n✅ Test data populated successfully!'))
        self.stdout.write('\nTest Credentials:')
        self.stdout.write('Admin: admin / admin123')
        self.stdout.write('Creator: creator1 / creator123')
        self.stdout.write('Explorer: explorer1 / explorer123')
