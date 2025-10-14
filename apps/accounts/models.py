from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    @property
    def is_explore_user(self):
        """Check if user is an explore user"""
        return self.user_type == self.UserType.EXPLORE

    @property
    def is_creation_user(self):
        """Check if user is a creation user"""
        return self.user_type == self.UserType.CREATION

    @property
    def is_admin_user(self):
        """Check if user is an admin user"""
        return self.user_type == self.UserType.ADMIN or self.is_superuser

    @property
    def can_create_places(self):
        """Check if user can create places"""
        return (
            self.user_type in [self.UserType.CREATION, self.UserType.ADMIN]
            or self.is_superuser
        )

    @property
    def can_moderate(self):
        """Check if user can moderate/approve places"""
        return self.user_type == self.UserType.ADMIN or self.is_superuser

    class Meta:
        ordering = ["-created_at"]
        verbose_name = "User"
        verbose_name_plural = "Users"

    class UserType(models.TextChoices):
        EXPLORE = "EXPLORE", "Explore User"
        CREATION = "CREATION", "Creation User"
        ADMIN = "ADMIN", "Admin User"

    def __str__(self):
        return f"{self.username} ({self.get_user_type_display()})"

    user_type = models.CharField(
        max_length=10,
        choices=UserType.choices,
        default=UserType.EXPLORE,
        help_text="Type of user account",
    )

    bio = models.TextField(blank=True, null=True, help_text="User biography")

    profile_picture = models.ImageField(
        upload_to="profiles/", blank=True, null=True, help_text="User profile picture"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
