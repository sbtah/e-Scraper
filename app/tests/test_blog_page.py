import pytest
from projects.models.blogs import BlogPage
from projects.models.webpages import WebPage


pytestmark = pytest.mark.django_db


class TestBlogPageModel:
    """Test cases for BlogPage object."""

    def test_blog_page_can_be_created(self, example_website):
        """Test that BlogPage object is created"""

        website = example_website
        assert BlogPage.objects.all().count() == 0
        blog_page = BlogPage.objects.create(
            discovery_url="http://test.com/",
            current_url="http://test.com/",
            is_active=True,
            seo_title="TestWeb",
            meta_description="Test Meta",
            canonical_url="http://test.com/",
            parrent_website=website,
            main_title="Our Test Blogs",
            main_description="Test...",
        )
        assert BlogPage.objects.all().count() == 1
        assert blog_page.parrent_website.domain == "test.com"
        assert isinstance(blog_page, BlogPage)
        assert isinstance(blog_page, WebPage)

    def test_discovery_url_must_be_unique(self, example_blog_page, example_website):
        """Test that each BlogPage have uniqe discovery_url"""

        website = example_website
        blog_page_1 = example_blog_page

        with pytest.raises(Exception):
            blog_page_2 = BlogPage.objects.create(
                discovery_url="http://test.com/",
                current_url="http://test.com/",
                is_active=True,
                seo_title="TestWeb",
                meta_description="Test Meta",
                canonical_url="http://test.com/",
                parrent_website=website,
                main_title="Our Test Blogs",
                main_description="Test...",
            )

    def test_str_method_returns_proper_data(sel, example_blog_page):
        """Test that __str__ for object is properly returning data."""

        blog_page = example_blog_page
        assert str(blog_page) == blog_page.discovery_url
