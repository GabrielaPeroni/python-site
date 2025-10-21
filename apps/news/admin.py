from django.contrib import admin

from .models import News, NewsCategory


@admin.register(NewsCategory)
class NewsCategoryAdmin(admin.ModelAdmin):
    list_display = ["name", "icon", "description"]
    search_fields = ["name", "description"]
    ordering = ["name"]


@admin.register(News)
class NewsAdmin(admin.ModelAdmin):
    list_display = [
        "title",
        "category",
        "status",
        "publish_date",
        "is_featured",
        "view_count",
        "author",
    ]
    list_filter = ["status", "category", "is_featured", "publish_date", "created_at"]
    search_fields = ["title", "content", "excerpt"]
    prepopulated_fields = {"slug": ("title",)}
    date_hierarchy = "publish_date"
    ordering = ["-publish_date", "-created_at"]

    fieldsets = [
        (
            "Basic Information",
            {
                "fields": ["title", "slug", "category", "content", "excerpt"],
            },
        ),
        (
            "Images",
            {
                "fields": ["featured_image", "image_caption"],
            },
        ),
        (
            "Event Details",
            {
                "fields": ["event_date", "event_end_date", "event_location"],
                "classes": ["collapse"],
                "description": "Fill these fields only if this is an event",
            },
        ),
        (
            "Publication",
            {
                "fields": ["status", "publish_date", "is_featured", "author"],
            },
        ),
        (
            "Metadata",
            {
                "fields": ["view_count", "created_at", "updated_at"],
                "classes": ["collapse"],
            },
        ),
    ]

    readonly_fields = ["created_at", "updated_at", "view_count"]

    def save_model(self, request, obj, form, change):
        """Set author to current user if creating new news"""
        if not change:  # If creating new object
            obj.author = request.user
        super().save_model(request, obj, form, change)
