from django.contrib.auth import get_user_model
from django.test import Client, TestCase
from django.urls import reverse

from .models import Category, Place, PlaceApproval, PlaceReview

User = get_user_model()


class CategoryModelTests(TestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Restaurants",
            slug="restaurants",
            description="Best dining spots",
            icon="🍽️",
            display_order=1,
        )

    def test_category_creation(self):
        """Test category is created correctly"""
        self.assertEqual(self.category.name, "Restaurants")
        self.assertEqual(self.category.slug, "restaurants")
        self.assertTrue(self.category.is_active)

    def test_category_string_representation(self):
        """Test category string representation"""
        self.assertEqual(str(self.category), "Restaurants")

    def test_active_places_count_property(self):
        """Test active_places_count property"""
        user = User.objects.create_user(username="creator", password="pass123")

        # Create approved place
        place1 = Place.objects.create(
            name="Test Place 1",
            description="Test description",
            address="Test address",
            created_by=user,
            is_approved=True,
            is_active=True,
        )
        place1.categories.add(self.category)

        # Create unapproved place
        place2 = Place.objects.create(
            name="Test Place 2",
            description="Test description",
            address="Test address",
            created_by=user,
            is_approved=False,
        )
        place2.categories.add(self.category)

        self.assertEqual(self.category.active_places_count, 1)

    def test_category_ordering(self):
        """Test categories are ordered by display_order and name"""
        cat2 = Category.objects.create(name="Hotels", slug="hotels", display_order=2)
        cat3 = Category.objects.create(name="Arts", slug="arts", display_order=1)

        categories = list(Category.objects.all())
        self.assertEqual(categories[0].display_order, 1)
        self.assertEqual(categories[1].display_order, 1)
        self.assertEqual(categories[2].display_order, 2)


class PlaceModelTests(TestCase):
    """Tests for Place model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="creator", password="pass123", user_type="CREATION"
        )
        self.category = Category.objects.create(name="Restaurants", slug="restaurants")

    def test_place_creation(self):
        """Test place is created correctly"""
        place = Place.objects.create(
            name="Test Restaurant",
            description="Great food",
            address="123 Main St",
            created_by=self.user,
        )
        self.assertEqual(place.name, "Test Restaurant")
        self.assertFalse(place.is_approved)  # Default should be False
        self.assertTrue(place.is_active)  # Default should be True
        self.assertEqual(place.created_by, self.user)

    def test_place_string_representation(self):
        """Test place string representation"""
        place = Place.objects.create(
            name="Test Place",
            description="Test",
            address="Test address",
            created_by=self.user,
        )
        self.assertEqual(str(place), "Test Place")

    def test_place_is_pending_property(self):
        """Test is_pending property"""
        place = Place.objects.create(
            name="Test Place",
            description="Test",
            address="Test address",
            created_by=self.user,
            is_approved=False,
        )
        self.assertTrue(place.is_pending)

        place.is_approved = True
        place.save()
        self.assertFalse(place.is_pending)

    def test_place_category_relationship(self):
        """Test many-to-many relationship with categories"""
        place = Place.objects.create(
            name="Test Place",
            description="Test",
            address="Test address",
            created_by=self.user,
        )
        place.categories.add(self.category)

        self.assertEqual(place.categories.count(), 1)
        self.assertIn(self.category, place.categories.all())


class PlaceImageModelTests(TestCase):
    """Tests for PlaceImage model"""

    def setUp(self):
        self.user = User.objects.create_user(username="creator", password="pass123")
        self.place = Place.objects.create(
            name="Test Place",
            description="Test",
            address="Test address",
            created_by=self.user,
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
            username="creator", password="pass123", user_type="CREATION"
        )
        self.admin = User.objects.create_user(
            username="admin", password="pass123", user_type="ADMIN"
        )
        self.place = Place.objects.create(
            name="Test Place",
            description="Test",
            address="Test address",
            created_by=self.creator,
            is_approved=False,
        )

    def test_place_approval_creation(self):
        """Test approval record is created"""
        approval = PlaceApproval.objects.create(
            place=self.place,
            reviewer=self.admin,
            action="APPROVE",
            comments="Looks good",
        )
        self.assertEqual(approval.place, self.place)
        self.assertEqual(approval.reviewer, self.admin)
        self.assertEqual(approval.action, "APPROVE")

    def test_approval_updates_place_status(self):
        """Test that approving updates place.is_approved"""
        approval = PlaceApproval.objects.create(
            place=self.place, reviewer=self.admin, action="APPROVE"
        )
        self.place.refresh_from_db()
        self.assertTrue(self.place.is_approved)

    def test_rejection_updates_place_status(self):
        """Test that rejecting updates place status"""
        approval = PlaceApproval.objects.create(
            place=self.place,
            reviewer=self.admin,
            action="REJECT",
            comments="Needs more information",
        )
        self.place.refresh_from_db()
        self.assertFalse(self.place.is_approved)
        self.assertFalse(self.place.is_active)


class ExploreViewTests(TestCase):
    """Tests for explore page views"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="creator", password="pass123", user_type="CREATION"
        )
        self.category = Category.objects.create(
            name="Restaurants", slug="restaurants", icon="🍽️"
        )

        # Create approved places
        for i in range(3):
            place = Place.objects.create(
                name=f"Place {i}",
                description="Test description",
                address="Test address",
                created_by=self.user,
                is_approved=True,
                is_active=True,
            )
            place.categories.add(self.category)

    def test_explore_page_loads(self):
        """Test explore page loads successfully"""
        response = self.client.get(reverse("explore:explore"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "explore/explore.html")

    def test_explore_page_shows_categories(self):
        """Test explore page displays categories"""
        response = self.client.get(reverse("explore:explore"))
        self.assertContains(response, "Restaurants")
        self.assertIn("categories", response.context)
        self.assertEqual(response.context["categories"].count(), 1)

    def test_explore_page_shows_approved_places_only(self):
        """Test explore page only shows approved places"""
        # Create unapproved place
        Place.objects.create(
            name="Unapproved Place",
            description="Test",
            address="Test address",
            created_by=self.user,
            is_approved=False,
        )

        response = self.client.get(reverse("explore:explore"))
        self.assertNotContains(response, "Unapproved Place")
        self.assertEqual(response.context["all_places"].count(), 3)

    def test_explore_page_sorting(self):
        """Test explore page sorting functionality"""
        # Test default sorting (newest first)
        response = self.client.get(reverse("explore:explore"))
        self.assertEqual(response.context["current_sort"], "-created_at")

        # Test name sorting
        response = self.client.get(reverse("explore:explore") + "?sort=name")
        self.assertEqual(response.context["current_sort"], "name")


class LandingPageTests(TestCase):
    """Tests for landing page"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="creator", password="pass123")

        # Create a place
        self.place = Place.objects.create(
            name="Featured Place",
            description="Test description",
            address="Test address",
            created_by=self.user,
            is_approved=True,
            is_active=True,
        )

    def test_landing_page_loads(self):
        """Test landing page loads successfully"""
        response = self.client.get(reverse("core:landing"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "core/landing.html")

    def test_landing_page_shows_featured_places(self):
        """Test landing page shows featured places"""
        response = self.client.get(reverse("core:landing"))
        self.assertIn("featured_places", response.context)
        self.assertContains(response, "Featured Place")


class PlaceCreateViewTests(TestCase):
    """Tests for place creation functionality"""

    def setUp(self):
        self.client = Client()
        self.creation_user = User.objects.create_user(
            username="creator", password="pass123", user_type="CREATION"
        )
        self.explore_user = User.objects.create_user(
            username="explorer", password="pass123", user_type="EXPLORE"
        )
        self.admin_user = User.objects.create_user(
            username="admin", password="pass123", user_type="ADMIN"
        )
        self.category = Category.objects.create(name="Restaurants", slug="restaurants")

    def test_place_create_view_requires_login(self):
        """Test place creation requires authentication"""
        response = self.client.get(reverse("explore:place_create"))
        self.assertRedirects(response, "/accounts/login/?next=/explore/place/create/")

    def test_explore_user_cannot_create_places(self):
        """Test explore users cannot access place creation"""
        self.client.login(username="explorer", password="pass123")
        response = self.client.get(reverse("explore:place_create"))
        self.assertRedirects(response, reverse("explore:explore"))

    def test_creation_user_can_access_place_create_form(self):
        """Test creation users can access place creation form"""
        self.client.login(username="creator", password="pass123")
        response = self.client.get(reverse("explore:place_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "explore/place_form.html")
        self.assertContains(response, "Adicionar Novo Lugar")

    def test_admin_user_can_access_place_create_form(self):
        """Test admin users can access place creation form"""
        self.client.login(username="admin", password="pass123")
        response = self.client.get(reverse("explore:place_create"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "explore/place_form.html")

    def test_place_creation_with_valid_data(self):
        """Test creating a place with valid data"""
        self.client.login(username="creator", password="pass123")

        form_data = {
            "name": "Test Restaurant",
            "description": "Great food and atmosphere",
            "address": "123 Main Street, Maricá, RJ",
            "categories": [self.category.id],
            # Formset management data
            "images-TOTAL_FORMS": "0",
            "images-INITIAL_FORMS": "0",
            "images-MIN_NUM_FORMS": "0",
            "images-MAX_NUM_FORMS": "10",
        }

        response = self.client.post(reverse("explore:place_create"), data=form_data)

        # Check place was created
        self.assertEqual(Place.objects.count(), 1)
        place = Place.objects.first()

        # Check place properties
        self.assertEqual(place.name, "Test Restaurant")
        self.assertEqual(place.created_by, self.creation_user)
        self.assertFalse(place.is_approved)  # Should start as unapproved
        self.assertTrue(place.is_active)
        self.assertIn(self.category, place.categories.all())

        # Check redirect
        self.assertRedirects(
            response, reverse("explore:place_detail", kwargs={"pk": place.pk})
        )

    def test_place_creation_with_invalid_data(self):
        """Test place creation with invalid data"""
        self.client.login(username="creator", password="pass123")

        # Missing required fields
        form_data = {
            "name": "",  # Required field missing
            "description": "",  # Required field missing
            "images-TOTAL_FORMS": "0",
            "images-INITIAL_FORMS": "0",
            "images-MIN_NUM_FORMS": "0",
            "images-MAX_NUM_FORMS": "10",
        }

        response = self.client.post(reverse("explore:place_create"), data=form_data)

        # Should not create place and should show form with errors
        self.assertEqual(Place.objects.count(), 0)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "explore/place_form.html")


class PlaceUpdateViewTests(TestCase):
    """Tests for place editing functionality"""

    def setUp(self):
        self.client = Client()
        self.creation_user = User.objects.create_user(
            username="creator", password="pass123", user_type="CREATION"
        )
        self.other_user = User.objects.create_user(
            username="other", password="pass123", user_type="CREATION"
        )
        self.admin_user = User.objects.create_user(
            username="admin", password="pass123", user_type="ADMIN"
        )
        self.category = Category.objects.create(name="Restaurants", slug="restaurants")

        self.place = Place.objects.create(
            name="Original Place",
            description="Original description",
            address="Original address",
            created_by=self.creation_user,
            is_approved=True,
        )
        self.place.categories.add(self.category)

    def test_place_update_requires_login(self):
        """Test place editing requires authentication"""
        response = self.client.get(
            reverse("explore:place_edit", kwargs={"pk": self.place.pk})
        )
        self.assertRedirects(
            response, f"/accounts/login/?next=/explore/place/{self.place.pk}/edit/"
        )

    def test_creator_can_edit_own_place(self):
        """Test place creator can edit their own place"""
        self.client.login(username="creator", password="pass123")
        response = self.client.get(
            reverse("explore:place_edit", kwargs={"pk": self.place.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "explore/place_form.html")
        self.assertContains(response, f"Editar {self.place.name}")

    def test_admin_can_edit_any_place(self):
        """Test admin users can edit any place"""
        self.client.login(username="admin", password="pass123")
        response = self.client.get(
            reverse("explore:place_edit", kwargs={"pk": self.place.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "explore/place_form.html")

    def test_other_creation_user_cannot_edit_place(self):
        """Test other creation users cannot edit places they didn't create"""
        self.client.login(username="other", password="pass123")
        response = self.client.get(
            reverse("explore:place_edit", kwargs={"pk": self.place.pk})
        )
        self.assertRedirects(
            response, reverse("explore:place_detail", kwargs={"pk": self.place.pk})
        )

    def test_place_update_with_valid_data(self):
        """Test updating a place with valid data"""
        self.client.login(username="creator", password="pass123")

        form_data = {
            "name": "Updated Place Name",
            "description": "Updated description",
            "address": "Updated address",
            "categories": [self.category.id],
            "images-TOTAL_FORMS": "0",
            "images-INITIAL_FORMS": "0",
            "images-MIN_NUM_FORMS": "0",
            "images-MAX_NUM_FORMS": "10",
        }

        response = self.client.post(
            reverse("explore:place_edit", kwargs={"pk": self.place.pk}), data=form_data
        )

        # Check place was updated
        self.place.refresh_from_db()
        self.assertEqual(self.place.name, "Updated Place Name")
        self.assertEqual(self.place.description, "Updated description")
        self.assertEqual(self.place.address, "Updated address")

        # Check redirect
        self.assertRedirects(
            response, reverse("explore:place_detail", kwargs={"pk": self.place.pk})
        )


class PlaceDeleteViewTests(TestCase):
    """Tests for place deletion functionality"""

    def setUp(self):
        self.client = Client()
        self.creation_user = User.objects.create_user(
            username="creator", password="pass123", user_type="CREATION"
        )
        self.other_user = User.objects.create_user(
            username="other", password="pass123", user_type="CREATION"
        )
        self.admin_user = User.objects.create_user(
            username="admin", password="pass123", user_type="ADMIN"
        )

        self.place = Place.objects.create(
            name="Test Place",
            description="Test description",
            address="Test address",
            created_by=self.creation_user,
        )

    def test_place_delete_requires_login(self):
        """Test place deletion requires authentication"""
        response = self.client.get(
            reverse("explore:place_delete", kwargs={"pk": self.place.pk})
        )
        self.assertRedirects(
            response, f"/accounts/login/?next=/explore/place/{self.place.pk}/delete/"
        )

    def test_place_delete_confirmation_page(self):
        """Test place deletion confirmation page loads"""
        self.client.login(username="creator", password="pass123")
        response = self.client.get(
            reverse("explore:place_delete", kwargs={"pk": self.place.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "explore/place_delete_confirm.html")
        self.assertContains(response, "Confirmar Exclusão")
        self.assertContains(response, self.place.name)

    def test_creator_can_delete_own_place(self):
        """Test place creator can delete their own place"""
        self.client.login(username="creator", password="pass123")
        response = self.client.post(
            reverse("explore:place_delete", kwargs={"pk": self.place.pk})
        )

        # Check place was deleted
        self.assertEqual(Place.objects.count(), 0)
        self.assertRedirects(response, reverse("explore:explore"))

    def test_admin_can_delete_any_place(self):
        """Test admin users can delete any place"""
        self.client.login(username="admin", password="pass123")
        response = self.client.post(
            reverse("explore:place_delete", kwargs={"pk": self.place.pk})
        )

        # Check place was deleted
        self.assertEqual(Place.objects.count(), 0)
        self.assertRedirects(response, reverse("explore:explore"))

    def test_other_user_cannot_delete_place(self):
        """Test other users cannot delete places they didn't create"""
        self.client.login(username="other", password="pass123")
        response = self.client.get(
            reverse("explore:place_delete", kwargs={"pk": self.place.pk})
        )
        # Should redirect to detail page or show error
        self.assertIn(response.status_code, [302, 403, 404])

        # Check place still exists
        self.assertEqual(Place.objects.count(), 1)


class PlaceDetailViewTests(TestCase):
    """Tests for place detail view functionality"""

    def setUp(self):
        self.client = Client()
        self.creation_user = User.objects.create_user(
            username="creator", password="pass123", user_type="CREATION"
        )
        self.admin_user = User.objects.create_user(
            username="admin", password="pass123", user_type="ADMIN"
        )
        self.explore_user = User.objects.create_user(
            username="explorer", password="pass123", user_type="EXPLORE"
        )

        self.approved_place = Place.objects.create(
            name="Approved Place",
            description="Approved description",
            address="Approved address",
            created_by=self.creation_user,
            is_approved=True,
            is_active=True,
        )

        self.unapproved_place = Place.objects.create(
            name="Unapproved Place",
            description="Unapproved description",
            address="Unapproved address",
            created_by=self.creation_user,
            is_approved=False,
            is_active=True,
        )

    def test_approved_place_visible_to_all(self):
        """Test approved places are visible to all users"""
        # Anonymous user
        response = self.client.get(
            reverse("explore:place_detail", kwargs={"pk": self.approved_place.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Approved Place")

        # Logged in explore user
        self.client.login(username="explorer", password="pass123")
        response = self.client.get(
            reverse("explore:place_detail", kwargs={"pk": self.approved_place.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_unapproved_place_visible_to_creator_and_admin(self):
        """Test unapproved places are only visible to creator and admin"""
        # Creator can see their own unapproved place
        self.client.login(username="creator", password="pass123")
        response = self.client.get(
            reverse("explore:place_detail", kwargs={"pk": self.unapproved_place.pk})
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Unapproved Place")

        # Admin can see any unapproved place
        self.client.login(username="admin", password="pass123")
        response = self.client.get(
            reverse("explore:place_detail", kwargs={"pk": self.unapproved_place.pk})
        )
        self.assertEqual(response.status_code, 200)

    def test_unapproved_place_hidden_from_explore_users(self):
        """Test unapproved places are hidden from explore users"""
        self.client.login(username="explorer", password="pass123")
        response = self.client.get(
            reverse("explore:place_detail", kwargs={"pk": self.unapproved_place.pk})
        )
        self.assertEqual(response.status_code, 404)

    def test_edit_button_shown_to_authorized_users(self):
        """Test edit button is shown to authorized users"""
        # Creator sees edit button
        self.client.login(username="creator", password="pass123")
        response = self.client.get(
            reverse("explore:place_detail", kwargs={"pk": self.approved_place.pk})
        )
        self.assertTrue(response.context["can_edit"])

        # Admin sees edit button
        self.client.login(username="admin", password="pass123")
        response = self.client.get(
            reverse("explore:place_detail", kwargs={"pk": self.approved_place.pk})
        )
        self.assertTrue(response.context["can_edit"])

        # Explore user doesn't see edit button
        self.client.login(username="explorer", password="pass123")
        response = self.client.get(
            reverse("explore:place_detail", kwargs={"pk": self.approved_place.pk})
        )
        self.assertFalse(response.context["can_edit"])


class CategoryDetailViewTests(TestCase):
    """Tests for category detail view"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username="creator", password="pass123")
        self.category = Category.objects.create(
            name="Restaurants", slug="restaurants", description="Best dining spots"
        )

        # Create approved places in category
        for i in range(3):
            place = Place.objects.create(
                name=f"Restaurant {i}",
                description="Test restaurant",
                address="Test address",
                created_by=self.user,
                is_approved=True,
                is_active=True,
            )
            place.categories.add(self.category)

        # Create unapproved place (should not appear)
        unapproved_place = Place.objects.create(
            name="Unapproved Restaurant",
            description="Test restaurant",
            address="Test address",
            created_by=self.user,
            is_approved=False,
        )
        unapproved_place.categories.add(self.category)

    def test_category_detail_page_loads(self):
        """Test category detail page loads successfully"""
        response = self.client.get(
            reverse("explore:category_detail", kwargs={"slug": "restaurants"})
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "explore/category_detail.html")

    def test_category_detail_shows_only_approved_places(self):
        """Test category detail page shows only approved places"""
        response = self.client.get(
            reverse("explore:category_detail", kwargs={"slug": "restaurants"})
        )
        self.assertEqual(response.context["places"].count(), 3)
        self.assertNotContains(response, "Unapproved Restaurant")

    def test_category_detail_sorting(self):
        """Test category detail page sorting"""
        response = self.client.get(
            reverse("explore:category_detail", kwargs={"slug": "restaurants"})
            + "?sort=name"
        )
        self.assertEqual(response.context["current_sort"], "name")

    def test_nonexistent_category_returns_404(self):
        """Test accessing nonexistent category returns 404"""
        response = self.client.get(
            reverse("explore:category_detail", kwargs={"slug": "nonexistent"})
        )
        self.assertEqual(response.status_code, 404)


class PlaceReviewModelTests(TestCase):
    """Tests for PlaceReview model"""

    def setUp(self):
        self.user = User.objects.create_user(
            username="reviewer", password="pass123", user_type="EXPLORE"
        )
        self.creator = User.objects.create_user(
            username="creator", password="pass123", user_type="CREATION"
        )
        self.place = Place.objects.create(
            name="Test Place",
            description="Test description",
            address="Test address",
            created_by=self.creator,
            is_approved=True,
            is_active=True,
        )

    def test_review_creation(self):
        """Test review is created correctly"""
        review = PlaceReview.objects.create(
            place=self.place,
            user=self.user,
            rating=5,
            comment="Excellent place!",
        )
        self.assertEqual(review.place, self.place)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Excellent place!")

    def test_review_string_representation(self):
        """Test review string representation"""
        review = PlaceReview.objects.create(
            place=self.place,
            user=self.user,
            rating=4,
            comment="Good place",
        )
        expected = f"{self.user.username} - {self.place.name} (4★)"
        self.assertEqual(str(review), expected)

    def test_unique_review_per_user_per_place(self):
        """Test one review per user per place constraint"""
        PlaceReview.objects.create(
            place=self.place,
            user=self.user,
            rating=5,
            comment="First review",
        )

        # Attempting to create second review for same user/place should fail
        with self.assertRaises(Exception):
            PlaceReview.objects.create(
                place=self.place,
                user=self.user,
                rating=3,
                comment="Second review",
            )

    def test_place_average_rating_property(self):
        """Test place average_rating property"""
        # No reviews
        self.assertIsNone(self.place.average_rating)

        # Add reviews
        user2 = User.objects.create_user(username="user2", password="pass123")
        user3 = User.objects.create_user(username="user3", password="pass123")

        PlaceReview.objects.create(
            place=self.place, user=self.user, rating=5, comment="Great!"
        )
        PlaceReview.objects.create(
            place=self.place, user=user2, rating=4, comment="Good"
        )
        PlaceReview.objects.create(place=self.place, user=user3, rating=3, comment="OK")

        # Average should be (5+4+3)/3 = 4.0
        self.assertEqual(self.place.average_rating, 4.0)

    def test_place_review_count_property(self):
        """Test place review_count property"""
        self.assertEqual(self.place.review_count, 0)

        PlaceReview.objects.create(
            place=self.place, user=self.user, rating=5, comment="Great!"
        )
        self.assertEqual(self.place.review_count, 1)

        user2 = User.objects.create_user(username="user2", password="pass123")
        PlaceReview.objects.create(
            place=self.place, user=user2, rating=4, comment="Good"
        )
        self.assertEqual(self.place.review_count, 2)


class PlaceReviewViewTests(TestCase):
    """Tests for place review functionality"""

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username="reviewer", password="pass123", user_type="EXPLORE"
        )
        self.creator = User.objects.create_user(
            username="creator", password="pass123", user_type="CREATION"
        )
        self.admin = User.objects.create_user(
            username="admin", password="pass123", user_type="ADMIN"
        )
        self.place = Place.objects.create(
            name="Test Place",
            description="Test description",
            address="Test address",
            created_by=self.creator,
            is_approved=True,
            is_active=True,
        )

    def test_review_create_requires_login(self):
        """Test creating a review requires authentication"""
        response = self.client.get(
            reverse("explore:review_create", kwargs={"place_pk": self.place.pk})
        )
        self.assertEqual(response.status_code, 302)  # Redirect to login

    def test_authenticated_user_can_create_review(self):
        """Test authenticated user can create a review"""
        self.client.login(username="reviewer", password="pass123")

        response = self.client.post(
            reverse("explore:review_create", kwargs={"place_pk": self.place.pk}),
            data={
                "rating": 5,
                "comment": "Excellent place!",
            },
        )

        # Check review was created
        self.assertEqual(PlaceReview.objects.count(), 1)
        review = PlaceReview.objects.first()
        self.assertEqual(review.place, self.place)
        self.assertEqual(review.user, self.user)
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Excellent place!")

        # Should redirect to place detail
        self.assertRedirects(
            response, reverse("explore:place_detail", kwargs={"pk": self.place.pk})
        )

    def test_user_cannot_create_duplicate_review(self):
        """Test user cannot review same place twice"""
        self.client.login(username="reviewer", password="pass123")

        # Create first review
        PlaceReview.objects.create(
            place=self.place,
            user=self.user,
            rating=5,
            comment="First review",
        )

        # Attempt to create second review
        response = self.client.post(
            reverse("explore:review_create", kwargs={"place_pk": self.place.pk}),
            data={
                "rating": 3,
                "comment": "Second review",
            },
        )

        # Should still have only one review
        self.assertEqual(PlaceReview.objects.count(), 1)

        # Should redirect back to place detail with warning
        self.assertRedirects(
            response, reverse("explore:place_detail", kwargs={"pk": self.place.pk})
        )

    def test_user_can_edit_own_review(self):
        """Test user can edit their own review"""
        review = PlaceReview.objects.create(
            place=self.place,
            user=self.user,
            rating=4,
            comment="Original comment",
        )

        self.client.login(username="reviewer", password="pass123")

        response = self.client.post(
            reverse("explore:review_edit", kwargs={"pk": review.pk}),
            data={
                "rating": 5,
                "comment": "Updated comment",
            },
        )

        # Check review was updated
        review.refresh_from_db()
        self.assertEqual(review.rating, 5)
        self.assertEqual(review.comment, "Updated comment")

        # Should redirect to place detail
        self.assertRedirects(
            response, reverse("explore:place_detail", kwargs={"pk": self.place.pk})
        )

    def test_user_cannot_edit_others_review(self):
        """Test user cannot edit another user's review"""
        other_user = User.objects.create_user(
            username="other", password="pass123", user_type="EXPLORE"
        )
        review = PlaceReview.objects.create(
            place=self.place,
            user=other_user,
            rating=4,
            comment="Other's review",
        )

        self.client.login(username="reviewer", password="pass123")

        response = self.client.get(
            reverse("explore:review_edit", kwargs={"pk": review.pk})
        )

        # Should be forbidden or redirect
        self.assertIn(response.status_code, [302, 403, 404])

    def test_admin_can_edit_any_review(self):
        """Test admin can edit any review"""
        review = PlaceReview.objects.create(
            place=self.place,
            user=self.user,
            rating=4,
            comment="Original comment",
        )

        self.client.login(username="admin", password="pass123")

        response = self.client.post(
            reverse("explore:review_edit", kwargs={"pk": review.pk}),
            data={
                "rating": 3,
                "comment": "Admin edited",
            },
        )

        # Check review was updated
        review.refresh_from_db()
        self.assertEqual(review.rating, 3)
        self.assertEqual(review.comment, "Admin edited")

    def test_user_can_delete_own_review(self):
        """Test user can delete their own review"""
        review = PlaceReview.objects.create(
            place=self.place,
            user=self.user,
            rating=4,
            comment="My review",
        )

        self.client.login(username="reviewer", password="pass123")

        response = self.client.post(
            reverse("explore:review_delete", kwargs={"pk": review.pk})
        )

        # Check review was deleted
        self.assertEqual(PlaceReview.objects.count(), 0)

        # Should redirect to place detail
        self.assertRedirects(
            response, reverse("explore:place_detail", kwargs={"pk": self.place.pk})
        )

    def test_admin_can_delete_any_review(self):
        """Test admin can delete any review"""
        review = PlaceReview.objects.create(
            place=self.place,
            user=self.user,
            rating=4,
            comment="User review",
        )

        self.client.login(username="admin", password="pass123")

        response = self.client.post(
            reverse("explore:review_delete", kwargs={"pk": review.pk})
        )

        # Check review was deleted
        self.assertEqual(PlaceReview.objects.count(), 0)

    def test_place_detail_shows_reviews(self):
        """Test place detail page shows reviews"""
        PlaceReview.objects.create(
            place=self.place,
            user=self.user,
            rating=5,
            comment="Great place!",
        )

        response = self.client.get(
            reverse("explore:place_detail", kwargs={"pk": self.place.pk})
        )

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Great place!")
        self.assertContains(response, self.user.username)
        self.assertIn("reviews", response.context)
        self.assertEqual(response.context["reviews"].count(), 1)

    def test_review_validation_requires_rating(self):
        """Test review form requires rating"""
        self.client.login(username="reviewer", password="pass123")

        response = self.client.post(
            reverse("explore:review_create", kwargs={"place_pk": self.place.pk}),
            data={
                "comment": "Comment without rating",
            },
        )

        # Should not create review
        self.assertEqual(PlaceReview.objects.count(), 0)

    def test_review_validation_requires_comment(self):
        """Test review form requires comment"""
        self.client.login(username="reviewer", password="pass123")

        response = self.client.post(
            reverse("explore:review_create", kwargs={"place_pk": self.place.pk}),
            data={
                "rating": 5,
                "comment": "",  # Empty comment
            },
        )

        # Should not create review
        self.assertEqual(PlaceReview.objects.count(), 0)
