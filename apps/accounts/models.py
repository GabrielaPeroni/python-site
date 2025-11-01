from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    @property
    def can_create_places(self):
        """Check if user can create places - all authenticated users can create"""
        return self.is_authenticated

    @property
    def can_moderate(self):
        """Check if user can moderate/approve places - only staff/superuser"""
        return self.is_staff or self.is_superuser

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    def __str__(self):
        return self.username

    bio = models.TextField(blank=True, null=True, help_text="User biography")

    profile_picture = models.ImageField(
        upload_to="profiles/", blank=True, null=True, help_text="User profile picture"
    )

    # Contact information
    contact_phone = models.CharField(
        max_length=20, blank=True, null=True, help_text="Contact phone number"
    )
    contact_email = models.EmailField(
        blank=True,
        null=True,
        help_text="Public contact email (different from login email)",
    )
    contact_website = models.URLField(
        blank=True, null=True, help_text="Website or social media URL"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
