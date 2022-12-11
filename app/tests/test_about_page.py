import pytest
from projects.models.about import AboutPage
from projects.models.webpages import WebPage


pytestmark = pytest.mark.django_db


class TestAboutPageModel:
    """Test cases for AboutPage object."""

    def test_about_page_can_be_created(self, example_website):
        """Test that AboutPage can be created"""

        website = example_website

        assert AboutPage.objects.all().count() == 0
        about_page = AboutPage.objects.create(
            discovery_url="http://test.com/about",
            current_url="http://test.com/about",
            is_active=True,
            seo_title="Test About",
            meta_description="Test Meta",
            canonical_url="http://test.com/",
            parrent_website=website,
            main_title="Test About",
            main_description="Sample about us text...",
        )
        assert AboutPage.objects.all().count() == 1
        assert about_page.parrent_website.domain == "test.com"
        assert isinstance(about_page, AboutPage)
        assert isinstance(about_page, WebPage)

    def test_discovery_url_must_be_unique(self, example_about_page, example_website):
        """Test that each BlogPage have uniqe discovery_url"""

        website = example_website
        about_page_1 = example_about_page
        with pytest.raises(Exception):
            about_page_2 = AboutPage.objects.create(
                discovery_url="http://test.com/about",
                current_url="http://test.com/about",
                is_active=True,
                seo_title="Test About",
                meta_description="Test Meta",
                canonical_url="http://test.com/",
                parrent_website=website,
                main_title="Test About",
                main_description="Sample about us text...",
            )

    def test_str_method_returns_proper_data(sel, example_about_page):
        """Test that __str__ for object is properly returning data."""

        about_page = example_about_page
        assert str(about_page) == about_page.main_title
