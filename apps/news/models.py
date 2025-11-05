from django.conf import settings
from django.db import models
from django.utils import timezone
from django.utils.text import slugify


class NewsCategory(models.Model):
    """Categories for news and events"""

    NEWS = "Noticias"
    EVENT = "Evento"
    ANNOUNCEMENT = "Anuncios"

    CATEGORY_CHOICES = [
        (NEWS, "Noticias"),
        (EVENT, "Eventos"),
        (ANNOUNCEMENT, "Anuncios"),
    ]

    name = models.CharField(max_length=50, choices=CATEGORY_CHOICES, unique=True)
    description = models.TextField(blank=True)
    icon = models.CharField(max_length=50, blank=True, help_text="Icone ou emoji")

    class Meta:
        verbose_name = "News Category"
        verbose_name_plural = "News Categories"
        ordering = ["name"]

    def __str__(self):
        return self.get_name_display()


class News(models.Model):
    """News and events for the city of Maricá"""

    DRAFT = "Em Progresso"
    PUBLISHED = "Publicado"
    ARCHIVED = "Arquivado"

    STATUS_CHOICES = [
        (DRAFT, "Em Progresso"),
        (PUBLISHED, "Publicado"),
        (ARCHIVED, "Arquivado"),
    ]

    # Basic fields
    title = models.CharField(max_length=200, help_text="Titulo da noticia ou evento")
    slug = models.SlugField(
        max_length=250, unique=True, blank=True, help_text="URL-friendly identifier"
    )
    content = models.TextField(help_text="Full content of the news or event")
    excerpt = models.TextField(
        max_length=300,
        blank=True,
        help_text="Short summary for listings (max 300 chars)",
    )

    # Categorization
    category = models.ForeignKey(
        NewsCategory,
        on_delete=models.PROTECT,
        related_name="news_items",
        help_text="Type of content (news, event, announcement)",
    )

    # Images
    featured_image = models.ImageField(
        upload_to="news/%Y/%m/",
        blank=True,
        null=True,
        help_text="Main image for the news/event",
    )
    image_caption = models.CharField(
        max_length=200, blank=True, help_text="Caption for featured image"
    )

    # Event-specific fields
    event_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="Date and time of event (for events only)",
    )
    event_location = models.CharField(
        max_length=200,
        blank=True,
        help_text="Location of event (for events only)",
    )
    event_end_date = models.DateTimeField(
        null=True,
        blank=True,
        help_text="End date and time of event (optional)",
    )

    # Publication management
    status = models.CharField(
        max_length=20,
        choices=STATUS_CHOICES,
        default=DRAFT,
        help_text="Publication status",
    )
    publish_date = models.DateTimeField(
        default=timezone.now,
        help_text="Date when this should be published",
    )

    # Author and metadata
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="news_items",
        help_text="User who created this news/event",
    )
    is_featured = models.BooleanField(
        default=False,
        help_text="Show in featured/highlighted sections",
    )
    view_count = models.PositiveIntegerField(
        default=0,
        help_text="Number of times this has been viewed",
    )

    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ["-publish_date", "-created_at"]
        verbose_name = "News/Event"
        verbose_name_plural = "News/Events"
        indexes = [
            models.Index(fields=["status", "-publish_date"]),
            models.Index(fields=["category", "status"]),
            models.Index(fields=["slug"]),
            models.Index(fields=["-publish_date"]),
        ]

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        """Auto-generate slug if not provided"""
        if not self.slug:
            base_slug = slugify(self.title)
            slug = base_slug
            counter = 1
            while News.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{counter}"
                counter += 1
            self.slug = slug

        # Auto-generate excerpt if not provided
        if not self.excerpt and self.content:
            self.excerpt = (
                self.content[:297] + "..." if len(self.content) > 300 else self.content
            )

        super().save(*args, **kwargs)

    @property
    def is_event(self):
        """Check if this is an event"""
        return self.category.name == NewsCategory.EVENT

    @property
    def is_upcoming_event(self):
        """Check if this is an upcoming event"""
        if not self.is_event or not self.event_date:
            return False
        return self.event_date > timezone.now()

    @property
    def is_past_event(self):
        """Check if this is a past event"""
        if not self.is_event or not self.event_date:
            return False
        return self.event_date <= timezone.now()

    def increment_view_count(self):
        """Increment the view counter"""
        self.view_count += 1
        self.save(update_fields=["view_count"])
