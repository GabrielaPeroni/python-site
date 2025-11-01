from django.test import Client, TestCase
from django.urls import reverse
from django.utils import timezone

from apps.accounts.models import User
from apps.news.models import News, NewsCategory


class NewsCategoryModelTests(TestCase):
    """Test suite for NewsCategory model"""

    def test_create_news_category(self):
        """Test creating a news category"""
        category = NewsCategory.objects.create(
            name=NewsCategory.NEWS, description="Latest news", icon="📰"
        )
        self.assertEqual(category.name, NewsCategory.NEWS)
        self.assertEqual(str(category), "News")

    def test_category_choices(self):
        """Test that all category choices work"""
        news_cat = NewsCategory.objects.create(name=NewsCategory.NEWS)
        event_cat = NewsCategory.objects.create(name=NewsCategory.EVENT)
        announcement_cat = NewsCategory.objects.create(name=NewsCategory.ANNOUNCEMENT)

        self.assertEqual(news_cat.get_name_display(), "News")
        self.assertEqual(event_cat.get_name_display(), "Event")
        self.assertEqual(announcement_cat.get_name_display(), "Announcement")


class NewsModelTests(TestCase):
    """Test suite for News model"""

    def setUp(self):
        """Set up test data"""
        self.user = User.objects.create_user(
            username="testauthor", password="testpass123", is_staff=True
        )
        self.category = NewsCategory.objects.create(
            name=NewsCategory.NEWS, description="Latest news"
        )

    def test_create_news(self):
        """Test creating a news article"""
        news = News.objects.create(
            title="Test News Article",
            content="This is test content",
            author=self.user,
            category=self.category,
            publish_date=timezone.now(),
            status=News.PUBLISHED,
        )
        self.assertEqual(news.title, "Test News Article")
        self.assertEqual(news.status, News.PUBLISHED)
        self.assertIsNotNone(news.slug)  # Auto-generated slug

    def test_news_string_representation(self):
        """Test the string representation of news"""
        news = News.objects.create(
            title="Test News",
            content="Content",
            author=self.user,
            category=self.category,
            publish_date=timezone.now(),
        )
        self.assertEqual(str(news), "Test News")

    def test_news_auto_slug_generation(self):
        """Test that slug is auto-generated from title"""
        news = News.objects.create(
            title="Test News Article",
            content="Content",
            author=self.user,
            category=self.category,
            publish_date=timezone.now(),
        )
        self.assertEqual(news.slug, "test-news-article")

    def test_news_defaults_to_draft(self):
        """Test that new news defaults to draft status"""
        news = News.objects.create(
            title="Draft News",
            content="Content",
            author=self.user,
            category=self.category,
            publish_date=timezone.now(),
        )
        self.assertEqual(news.status, News.DRAFT)

    def test_news_is_event_property(self):
        """Test is_event property for event category"""
        event_category = NewsCategory.objects.create(name=NewsCategory.EVENT)

        news = News.objects.create(
            title="Regular News",
            content="Content",
            author=self.user,
            category=self.category,
            publish_date=timezone.now(),
        )

        event = News.objects.create(
            title="Event News",
            content="Content",
            author=self.user,
            category=event_category,
            publish_date=timezone.now(),
            event_date=timezone.now(),
        )

        self.assertFalse(news.is_event)
        self.assertTrue(event.is_event)


class NewsListViewTests(TestCase):
    """Test suite for news list view"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.url = reverse("news:news_list")
        self.user = User.objects.create_user(
            username="testauthor", password="testpass123"
        )
        self.category = NewsCategory.objects.create(name=NewsCategory.NEWS)

        # Create published news
        self.published_news = News.objects.create(
            title="Published News",
            content="Published content",
            author=self.user,
            category=self.category,
            publish_date=timezone.now(),
            status=News.PUBLISHED,
        )

        # Create draft news (should not appear)
        self.draft_news = News.objects.create(
            title="Draft News",
            content="Draft content",
            author=self.user,
            category=self.category,
            publish_date=timezone.now(),
            status=News.DRAFT,
        )

    def test_news_list_page_loads(self):
        """Test that news list page loads successfully"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "news/news_list.html")

    def test_news_list_shows_published_only(self):
        """Test that only published news are shown"""
        response = self.client.get(self.url)
        self.assertContains(response, "Published News")
        self.assertNotContains(response, "Draft News")

    def test_news_list_ordered_by_date(self):
        """Test that news are ordered by publish date (newest first)"""
        # Create older news
        older_news = News.objects.create(
            title="Older News",
            content="Content",
            author=self.user,
            category=self.category,
            publish_date=timezone.now() - timezone.timedelta(days=5),
            status=News.PUBLISHED,
        )

        response = self.client.get(self.url)
        news_items = list(response.context["news_items"])

        # Newest should be first
        self.assertEqual(news_items[0].title, "Published News")
        self.assertEqual(news_items[1].title, "Older News")


class NewsDetailViewTests(TestCase):
    """Test suite for news detail view"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(username="testauthor")
        self.category = NewsCategory.objects.create(name=NewsCategory.NEWS)

        self.news = News.objects.create(
            title="Test News Article",
            slug="test-news-article",
            content="This is the full content of the news article",
            excerpt="This is a short excerpt",
            author=self.user,
            category=self.category,
            publish_date=timezone.now(),
            status=News.PUBLISHED,
        )
        self.url = reverse("news:news_detail", kwargs={"slug": self.news.slug})

    def test_news_detail_page_loads(self):
        """Test that news detail page loads successfully"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "news/news_detail.html")

    def test_news_detail_shows_content(self):
        """Test that news detail page shows full content"""
        response = self.client.get(self.url)
        self.assertContains(response, "Test News Article")
        self.assertContains(response, "This is the full content")

    def test_news_detail_shows_author(self):
        """Test that news detail page shows author"""
        response = self.client.get(self.url)
        self.assertContains(response, "testauthor")

    def test_news_detail_increments_view_count(self):
        """Test that viewing news increments view count"""
        initial_count = self.news.view_count
        self.client.get(self.url)

        # Refresh from database
        self.news.refresh_from_db()
        self.assertEqual(self.news.view_count, initial_count + 1)

    def test_news_detail_404_for_invalid_slug(self):
        """Test that invalid slug returns 404"""
        response = self.client.get(
            reverse("news:news_detail", kwargs={"slug": "non-existent"})
        )
        self.assertEqual(response.status_code, 404)


class NewsFeaturedTests(TestCase):
    """Test suite for featured news functionality"""

    def setUp(self):
        """Set up test data"""
        self.client = Client()
        self.user = User.objects.create_user(username="testauthor")
        self.category = NewsCategory.objects.create(name=NewsCategory.NEWS)

    def test_featured_news_appears_in_context(self):
        """Test that featured news are available in context"""
        # Create featured news
        featured_news = News.objects.create(
            title="Featured News",
            content="Content",
            author=self.user,
            category=self.category,
            publish_date=timezone.now(),
            status=News.PUBLISHED,
            is_featured=True,
        )

        response = self.client.get(reverse("news:news_list"))

        # Featured items should be in context
        self.assertIn("featured_items", response.context)
        featured_items = list(response.context["featured_items"])

        # Should contain our featured news
        self.assertEqual(len(featured_items), 1)
        self.assertEqual(featured_items[0].title, "Featured News")
