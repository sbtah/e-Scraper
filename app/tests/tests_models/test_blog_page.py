import pytest
from projects.models.blogs import BlogPage
from projects.models.webpages import WebPage


pytestmark = pytest.mark.django_db


class TestBlogPageModel:
    """Test cases for BlogPage object."""

    def test_blog_page_can_be_created(
        self, example_website, blog_page_create_test_data
    ):
        """Test that BlogPage object is created"""

        website = example_website
        creation_data = blog_page_create_test_data

        assert BlogPage.objects.all().count() == 0
        blog_page = BlogPage.objects.create(
            discovery_url=creation_data["discovery_url"],
            current_url=creation_data["current_url"],
            is_active=creation_data["is_active"],
            seo_title=creation_data["seo_title"],
            meta_description=creation_data["meta_description"],
            canonical_url=creation_data["canonical_url"],
            parrent_website=website,
            main_title=creation_data["main_title"],
            main_description=creation_data["main_description"],
        )
        assert BlogPage.objects.all().count() == 1
        assert blog_page.parrent_website.domain == "test.com"
        assert isinstance(blog_page, BlogPage)
        assert isinstance(blog_page, WebPage)

        assert blog_page.discovery_url == creation_data["discovery_url"]
        assert isinstance(blog_page.discovery_url, str)
        assert type(blog_page.discovery_url) == type(creation_data["discovery_url"])

        assert blog_page.current_url == creation_data["current_url"]
        assert isinstance(blog_page.current_url, str)
        assert type(blog_page.current_url) == type(creation_data["current_url"])

        assert blog_page.is_active == creation_data["is_active"]
        assert isinstance(blog_page.is_active, bool)
        assert type(blog_page.is_active) == type(creation_data["is_active"])

        assert blog_page.seo_title == creation_data["seo_title"]
        assert isinstance(blog_page.seo_title, str)
        assert type(blog_page.seo_title) == type(creation_data["seo_title"])

        assert blog_page.meta_description == creation_data["meta_description"]
        assert isinstance(blog_page.meta_description, str)
        assert type(blog_page.meta_description) == type(
            creation_data["meta_description"]
        )

        assert blog_page.canonical_url == creation_data["canonical_url"]
        assert isinstance(blog_page.canonical_url, str)
        assert type(blog_page.canonical_url) == type(creation_data["canonical_url"])

        assert blog_page.main_title == creation_data["main_title"]
        assert isinstance(blog_page.main_title, str)
        assert type(blog_page.main_title) == type(creation_data["main_title"])

        assert blog_page.main_description == creation_data["main_description"]
        assert isinstance(blog_page.main_description, str)
        assert type(blog_page.main_description) == type(
            creation_data["main_description"]
        )

    @pytest.mark.django_db(transaction=True)
    def test_discovery_url_must_be_unique(self, example_blog_page, example_website):
        """Test that each BlogPage have unique discovery_url"""

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
        assert BlogPage.objects.all().count() == 1

    def test_str_method_returns_proper_data(sel, example_blog_page):
        """Test that __str__ for object is properly returning data."""

        blog_page = example_blog_page
        assert str(blog_page) == blog_page.discovery_url
