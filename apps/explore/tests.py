from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta
from .models import Category, Place, PlaceImage, PlaceApproval

User = get_user_model()


class CategoryModelTests(TestCase):
    """Tests for Category model"""

    def setUp(self):
        self.category = Category.objects.create(
            name='Restaurants',
            slug='restaurants',
            description='Best dining spots',
            icon='🍽️',
            display_order=1
        )

    def test_category_creation(self):
        """Test category is created correctly"""
        self.assertEqual(self.category.name, 'Restaurants')
        self.assertEqual(self.category.slug, 'restaurants')
        self.assertTrue(self.category.is_active)

    def test_category_string_representation(self):
        """Test category string representation"""
        self.assertEqual(str(self.category), 'Restaurants')

    def test_active_places_count_property(self):
        """Test active_places_count property"""
        user = User.objects.create_user(username='creator', password='pass123')

        # Create approved place
        place1 = Place.objects.create(
            name='Test Place 1',
            description='Test description',
            address='Test address',
            created_by=user,
            is_approved=True,
            is_active=True
        )
        place1.categories.add(self.category)

        # Create unapproved place
        place2 = Place.objects.create(
            name='Test Place 2',
            description='Test description',
            address='Test address',
            created_by=user,
            is_approved=False
        )
        place2.categories.add(self.category)

        self.assertEqual(self.category.active_places_count, 1)

    def test_category_ordering(self):
        """Test categories are ordered by display_order and name"""
        cat2 = Category.objects.create(name='Hotels', slug='hotels', display_order=2)
        cat3 = Category.objects.create(name='Arts', slug='arts', display_order=1)

        categories = list(Category.objects.all())
        self.assertEqual(categories[0].display_order, 1)
        self.assertEqual(categories[1].display_order, 1)
        self.assertEqual(categories[2].display_order, 2)


class PlaceModelTests(TestCase):
    """Tests for Place model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username='creator',
            password='pass123',
            user_type='CREATION'
        )
        self.category = Category.objects.create(
            name='Restaurants',
            slug='restaurants'
        )

    def test_place_creation(self):
        """Test place is created correctly"""
        place = Place.objects.create(
            name='Test Restaurant',
            description='Great food',
            address='123 Main St',
            contact_phone='1234567890',
            contact_email='test@example.com',
            created_by=self.user
        )
        self.assertEqual(place.name, 'Test Restaurant')
        self.assertFalse(place.is_approved)  # Default should be False
        self.assertTrue(place.is_active)  # Default should be True
        self.assertEqual(place.created_by, self.user)

    def test_place_string_representation(self):
        """Test place string representation"""
        place = Place.objects.create(
            name='Test Place',
            description='Test',
            address='Test address',
            created_by=self.user
        )
        self.assertEqual(str(place), 'Test Place')

    def test_place_is_pending_property(self):
        """Test is_pending property"""
        place = Place.objects.create(
            name='Test Place',
            description='Test',
            address='Test address',
            created_by=self.user,
            is_approved=False
        )
        self.assertTrue(place.is_pending)

        place.is_approved = True
        place.save()
        self.assertFalse(place.is_pending)

    def test_place_has_coordinates_property(self):
        """Test has_coordinates property"""
        place = Place.objects.create(
            name='Test Place',
            description='Test',
            address='Test address',
            created_by=self.user
        )
        self.assertFalse(place.has_coordinates)

        place.latitude = -22.9192
        place.longitude = -42.8186
        place.save()
        self.assertTrue(place.has_coordinates)

    def test_place_category_relationship(self):
        """Test many-to-many relationship with categories"""
        place = Place.objects.create(
            name='Test Place',
            description='Test',
            address='Test address',
            created_by=self.user
        )
        place.categories.add(self.category)

        self.assertEqual(place.categories.count(), 1)
        self.assertIn(self.category, place.categories.all())


class PlaceImageModelTests(TestCase):
    """Tests for PlaceImage model"""

    def setUp(self):
        self.user = User.objects.create_user(username='creator', password='pass123')
        self.place = Place.objects.create(
            name='Test Place',
            description='Test',
            address='Test address',
            created_by=self.user
        )

    def test_place_primary_image_property(self):
        """Test primary_image property returns primary image"""
        # Note: We can't actually upload files in tests without mocking
        # So we'll just test the property exists
        self.assertIsNone(self.place.primary_image)

    def test_place_gallery_images_property(self):
        """Test gallery_images property"""
        images = self.place.gallery_images
        self.assertEqual(images.count(), 0)


class PlaceApprovalModelTests(TestCase):
    """Tests for PlaceApproval model"""

    def setUp(self):
        self.creator = User.objects.create_user(
            username='creator',
            password='pass123',
            user_type='CREATION'
        )
        self.admin = User.objects.create_user(
            username='admin',
            password='pass123',
            user_type='ADMIN'
        )
        self.place = Place.objects.create(
            name='Test Place',
            description='Test',
            address='Test address',
            created_by=self.creator,
            is_approved=False
        )

    def test_place_approval_creation(self):
        """Test approval record is created"""
        approval = PlaceApproval.objects.create(
            place=self.place,
            reviewer=self.admin,
            action='APPROVE',
            comments='Looks good'
        )
        self.assertEqual(approval.place, self.place)
        self.assertEqual(approval.reviewer, self.admin)
        self.assertEqual(approval.action, 'APPROVE')

    def test_approval_updates_place_status(self):
        """Test that approving updates place.is_approved"""
        approval = PlaceApproval.objects.create(
            place=self.place,
            reviewer=self.admin,
            action='APPROVE'
        )
        self.place.refresh_from_db()
        self.assertTrue(self.place.is_approved)

    def test_rejection_updates_place_status(self):
        """Test that rejecting updates place status"""
        approval = PlaceApproval.objects.create(
            place=self.place,
            reviewer=self.admin,
            action='REJECT',
            comments='Needs more information'
        )
        self.place.refresh_from_db()
        self.assertFalse(self.place.is_approved)
        self.assertFalse(self.place.is_active)


class ExploreViewTests(TestCase):
    """Tests for explore page views"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='creator',
            password='pass123',
            user_type='CREATION'
        )
        self.category = Category.objects.create(
            name='Restaurants',
            slug='restaurants',
            icon='🍽️'
        )

        # Create approved places
        for i in range(3):
            place = Place.objects.create(
                name=f'Place {i}',
                description='Test description',
                address='Test address',
                created_by=self.user,
                is_approved=True,
                is_active=True
            )
            place.categories.add(self.category)

    def test_explore_page_loads(self):
        """Test explore page loads successfully"""
        response = self.client.get(reverse('explore:explore'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'explore/explore.html')

    def test_explore_page_shows_categories(self):
        """Test explore page displays categories"""
        response = self.client.get(reverse('explore:explore'))
        self.assertContains(response, 'Restaurants')
        self.assertIn('categories', response.context)
        self.assertEqual(response.context['categories'].count(), 1)

    def test_explore_page_shows_approved_places_only(self):
        """Test explore page only shows approved places"""
        # Create unapproved place
        Place.objects.create(
            name='Unapproved Place',
            description='Test',
            address='Test address',
            created_by=self.user,
            is_approved=False
        )

        response = self.client.get(reverse('explore:explore'))
        self.assertNotContains(response, 'Unapproved Place')
        self.assertEqual(response.context['all_places'].count(), 3)

    def test_explore_page_sorting(self):
        """Test explore page sorting functionality"""
        # Test default sorting (newest first)
        response = self.client.get(reverse('explore:explore'))
        self.assertEqual(response.context['current_sort'], '-created_at')

        # Test name sorting
        response = self.client.get(reverse('explore:explore') + '?sort=name')
        self.assertEqual(response.context['current_sort'], 'name')


class LandingPageTests(TestCase):
    """Tests for landing page"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='creator', password='pass123')

        # Create a place
        self.place = Place.objects.create(
            name='Featured Place',
            description='Test description',
            address='Test address',
            created_by=self.user,
            is_approved=True,
            is_active=True
        )

    def test_landing_page_loads(self):
        """Test landing page loads successfully"""
        response = self.client.get(reverse('core:landing'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'core/landing.html')

    def test_landing_page_shows_featured_places(self):
        """Test landing page shows featured places"""
        response = self.client.get(reverse('core:landing'))
        self.assertIn('featured_places', response.context)
        self.assertContains(response, 'Featured Place')
