import pytest
from projects.models.about import AboutPage
from projects.models.webpages import WebPage


pytestmark = pytest.mark.django_db


class TestAboutPageModel:
    """Test cases for AboutPage object."""

    def test_about_page_can_be_created(
        self, example_website, about_page_create_test_data
    ):
        """Test that AboutPage can be created"""

        website = example_website
        creation_data = about_page_create_test_data

        assert AboutPage.objects.all().count() == 0
        about_page = AboutPage.objects.create(
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
        assert AboutPage.objects.all().count() == 1
        assert about_page.parrent_website.domain == "test.com"
        assert isinstance(about_page, AboutPage)
        assert isinstance(about_page, WebPage)

        assert about_page.discovery_url == creation_data["discovery_url"]
        assert isinstance(about_page.discovery_url, str)
        assert type(about_page.discovery_url) == type(creation_data["discovery_url"])

        assert about_page.current_url == creation_data["current_url"]
        assert isinstance(about_page.current_url, str)
        assert type(about_page.current_url) == type(creation_data["current_url"])

        assert about_page.is_active == creation_data["is_active"]
        assert isinstance(about_page.is_active, bool)
        assert type(about_page.is_active) == type(creation_data["is_active"])

        assert about_page.seo_title == creation_data["seo_title"]
        assert isinstance(about_page.seo_title, str)
        assert type(about_page.seo_title) == type(creation_data["seo_title"])

        assert about_page.meta_description == creation_data["meta_description"]
        assert isinstance(about_page.meta_description, str)
        assert type(about_page.meta_description) == type(
            creation_data["meta_description"]
        )

        assert about_page.canonical_url == creation_data["canonical_url"]
        assert isinstance(about_page.canonical_url, str)
        assert type(about_page.canonical_url) == type(creation_data["canonical_url"])

        assert about_page.main_title == creation_data["main_title"]
        assert isinstance(about_page.main_title, str)
        assert type(about_page.main_title) == type(creation_data["main_title"])

        assert about_page.main_description == creation_data["main_description"]
        assert isinstance(about_page.main_description, str)
        assert type(about_page.main_description) == type(
            creation_data["main_description"]
        )

    @pytest.mark.django_db(transaction=True)
    def test_discovery_url_must_be_unique(self, example_about_page, example_website):
        """Test that each BlogPage have unique discovery_url"""

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
        assert AboutPage.objects.all().count() == 1

    def test_str_method_returns_proper_data(sel, example_about_page):
        """Test that __str__ for object is properly returning data."""

        about_page = example_about_page
        assert str(about_page) == about_page.main_title
