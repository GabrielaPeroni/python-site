from django.conf import settings
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100, unique=True, help_text="Category name")

    slug = models.SlugField(
        max_length=100, unique=True, help_text="URL-friendly category identifier"
    )

    description = models.TextField(blank=True, help_text="Category description")

    icon = models.CharField(
        max_length=50, blank=True, help_text="Icon class or emoji for the category"
    )

    is_active = models.BooleanField(
        default=True, help_text="Whether the category is currently active"
    )

    display_order = models.IntegerField(
        default=0, help_text="Order in which category appears (lower numbers first)"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["display_order", "name"]
        verbose_name = "Category"
        verbose_name_plural = "Categories"
        indexes = [
            models.Index(fields=["is_active", "display_order"]),
            models.Index(fields=["slug"]),
        ]

    def __str__(self):
        return self.name

    @property
    def active_places_count(self):
        """Count of active approved places in this category"""
        return self.places.filter(is_active=True, is_approved=True).count()


class Place(models.Model):
    name = models.CharField(max_length=200, help_text="Name of the place")

    description = models.TextField(help_text="Detailed description of the place")

    address = models.TextField(help_text="Full address of the place")

    # Relationships
    categories = models.ManyToManyField(
        Category,
        related_name="places",
        blank=True,
        help_text="Categories this place belongs to",
    )

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="places",
        help_text="User who created this place",
    )

    # Status fields
    is_approved = models.BooleanField(
        default=False, help_text="Whether the place has been approved by admin"
    )

    is_active = models.BooleanField(
        default=True, help_text="Whether the place is currently active"
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Place"
        verbose_name_plural = "Places"
        indexes = [
            models.Index(fields=["is_approved", "is_active"]),
            models.Index(fields=["-created_at"]),
        ]

    def __str__(self):
        return self.name

    @property
    def is_pending(self):
        return not self.is_approved

    @property
    def primary_image(self):
        return self.images.filter(is_primary=True).first()

    @property
    def gallery_images(self):
        return self.images.all()

    @property
    def average_rating(self):
        """Calculate average rating from all reviews"""
        from django.db.models import Avg

        result = self.reviews.aggregate(Avg("rating"))
        return round(result["rating__avg"], 1) if result["rating__avg"] else None

    @property
    def review_count(self):
        """Count of reviews for this place"""
        return self.reviews.count()


class PlaceImage(models.Model):
    class Meta:
        ordering = ["display_order", "-uploaded_at"]
        verbose_name = "Place Image"
        verbose_name_plural = "Place Images"
        indexes = [
            models.Index(fields=["place", "display_order"]),
            models.Index(fields=["place", "is_primary"]),
        ]

    def __str__(self):
        return f"{self.place.name} - Image {self.id}"

    def save(self, *args, **kwargs):
        if self.is_primary:
            # Set all other images for this place to non-primary
            PlaceImage.objects.filter(place=self.place, is_primary=True).update(
                is_primary=False
            )
        super().save(*args, **kwargs)

    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name="images",
        help_text="Place this image belongs to",
    )

    image = models.ImageField(upload_to="places/images/%Y/%m/", help_text="Place image")

    caption = models.CharField(
        max_length=200, blank=True, help_text="Image caption or description"
    )

    is_primary = models.BooleanField(
        default=False, help_text="Whether this is the primary/main image for the place"
    )

    display_order = models.IntegerField(
        default=0,
        help_text="Order in which image appears in gallery (lower numbers first)",
    )

    uploaded_at = models.DateTimeField(
        auto_now_add=True, help_text="When the image was uploaded"
    )


class PlaceApproval(models.Model):
    class ActionType(models.TextChoices):
        APPROVE = "APPROVE", "Approved"
        REJECT = "REJECT", "Rejected"
        REQUEST_CHANGES = "REQUEST_CHANGES", "Request Changes"

    class Meta:
        ordering = ["-reviewed_at"]
        verbose_name = "Place Approval"
        verbose_name_plural = "Place Approvals"
        indexes = [
            models.Index(fields=["place", "-reviewed_at"]),
            models.Index(fields=["reviewer", "-reviewed_at"]),
            models.Index(fields=["action"]),
        ]

    def __str__(self):
        return f"{self.place.name} - {self.get_action_display()} by {self.reviewer}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        if self.action == self.ActionType.APPROVE:
            self.place.is_approved = True
            self.place.save(update_fields=["is_approved", "updated_at"])
        elif self.action == self.ActionType.REJECT:
            self.place.is_approved = False
            self.place.is_active = False
            self.place.save(update_fields=["is_approved", "is_active", "updated_at"])

    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name="approval_history",
        help_text="Place being reviewed",
    )

    reviewer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.SET_NULL,
        null=True,
        related_name="place_reviews",
        help_text="Admin user who reviewed the place",
    )

    action = models.CharField(
        max_length=20,
        choices=ActionType.choices,
        help_text="Action taken by the reviewer",
    )

    comments = models.TextField(blank=True, help_text="Reviewer comments or feedback")

    reviewed_at = models.DateTimeField(
        auto_now_add=True, help_text="When the review was conducted"
    )


class PlaceReview(models.Model):
    """User reviews and ratings for places"""

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "Place Review"
        verbose_name_plural = "Place Reviews"
        unique_together = [["place", "user"]]  # One review per user per place
        indexes = [
            models.Index(fields=["place", "-created_at"]),
            models.Index(fields=["user", "-created_at"]),
            models.Index(fields=["rating"]),
        ]

    def __str__(self):
        return f"{self.user.username} - {self.place.name} ({self.rating}★)"

    place = models.ForeignKey(
        Place,
        on_delete=models.CASCADE,
        related_name="reviews",
        help_text="Place being reviewed",
    )

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="place_reviews_written",
        help_text="User who wrote the review",
    )

    rating = models.IntegerField(
        choices=[
            (1, "1 Star"),
            (2, "2 Stars"),
            (3, "3 Stars"),
            (4, "4 Stars"),
            (5, "5 Stars"),
        ],
        help_text="Rating from 1 to 5 stars",
    )

    comment = models.TextField(
        help_text="Review comment/feedback",
        max_length=1000,
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
