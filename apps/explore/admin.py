from django.contrib import admin

from .models import Category, Place, PlaceApproval, PlaceImage


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "slug",
        "display_order",
        "is_active",
        "active_places_count",
        "created_at",
    )

    list_filter = ("is_active", "created_at")

    search_fields = ("name", "slug", "description")

    readonly_fields = ("created_at", "updated_at")

    prepopulated_fields = {"slug": ("name",)}

    fieldsets = (
        ("Basic Information", {"fields": ("name", "slug", "description", "icon")}),
        ("Display Settings", {"fields": ("display_order", "is_active")}),
        (
            "Timestamps",
            {"fields": ("created_at", "updated_at"), "classes": ("collapse",)},
        ),
    )


class PlaceImageInline(admin.TabularInline):
    model = PlaceImage
    extra = 1
    fields = ("image", "caption", "is_primary", "display_order")
    readonly_fields = ("uploaded_at",)


@admin.register(Place)
class PlaceAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.created_by = request.user
        super().save_model(request, obj, form, change)

    inlines = [PlaceImageInline]

    list_display = ("name", "created_by", "is_approved", "is_active", "created_at")

    list_filter = ("is_approved", "is_active", "categories", "created_at", "updated_at")

    search_fields = ("name", "description", "address", "created_by__username")

    readonly_fields = ("created_at", "updated_at", "created_by")

    fieldsets = (
        (
            "Basic Information",
            {"fields": ("name", "description", "address", "categories")},
        ),
        (
            "Contact Information",
            {"fields": ("contact_phone", "contact_email", "contact_website")},
        ),
        ("Location", {"fields": ("latitude", "longitude"), "classes": ("collapse",)}),
        ("Status", {"fields": ("is_approved", "is_active")}),
        (
            "Metadata",
            {
                "fields": ("created_by", "created_at", "updated_at"),
                "classes": ("collapse",),
            },
        ),
    )


@admin.register(PlaceImage)
class PlaceImageAdmin(admin.ModelAdmin):
    list_display = ("place", "caption", "is_primary", "display_order", "uploaded_at")

    list_filter = ("is_primary", "uploaded_at", "place")

    search_fields = ("place__name", "caption")

    readonly_fields = ("uploaded_at",)

    fieldsets = (
        ("Image Information", {"fields": ("place", "image", "caption")}),
        ("Display Settings", {"fields": ("is_primary", "display_order")}),
        ("Timestamp", {"fields": ("uploaded_at",)}),
    )


@admin.register(PlaceApproval)
class PlaceApprovalAdmin(admin.ModelAdmin):
    def save_model(self, request, obj, form, change):
        if not change:  # If creating new object
            obj.reviewer = request.user
        super().save_model(request, obj, form, change)

    list_display = ("place", "action", "reviewer", "reviewed_at")

    list_filter = ("action", "reviewed_at", "reviewer")

    search_fields = ("place__name", "reviewer__username", "comments")

    readonly_fields = ("reviewed_at",)

    fieldsets = (
        ("Review Information", {"fields": ("place", "action", "reviewer", "comments")}),
        ("Timestamp", {"fields": ("reviewed_at",)}),
    )
