import pytest
from projects.models.home import HomePage
from projects.models.webpages import WebPage


pytestmark = pytest.mark.django_db


class TestHomePageModel:
    """Test cases for HomePage object."""

    def test_home_page_can_be_created(
        self, example_website, home_page_create_test_data
    ):
        """Test that HomePage is created with proper values and types."""

        website = example_website
        creation_data = home_page_create_test_data

        assert HomePage.objects.all().count() == 0
        home_page = HomePage.objects.create(
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
        assert HomePage.objects.all().count() == 1
        assert home_page.parrent_website.domain == "test.com"
        assert isinstance(home_page, HomePage)
        assert isinstance(home_page, WebPage)

        assert home_page.discovery_url == creation_data["discovery_url"]
        assert isinstance(home_page.discovery_url, str)
        assert type(home_page.discovery_url) == type(creation_data["discovery_url"])

        assert home_page.current_url == creation_data["current_url"]
        assert isinstance(home_page.current_url, str)
        assert type(home_page.current_url) == type(creation_data["current_url"])

        assert home_page.is_active == creation_data["is_active"]
        assert isinstance(home_page.is_active, bool)
        assert type(home_page.is_active) == type(creation_data["is_active"])

        assert home_page.seo_title == creation_data["seo_title"]
        assert isinstance(home_page.seo_title, str)
        assert type(home_page.seo_title) == type(creation_data["seo_title"])

        assert home_page.meta_description == creation_data["meta_description"]
        assert isinstance(home_page.meta_description, str)
        assert type(home_page.meta_description) == type(
            creation_data["meta_description"]
        )

        assert home_page.canonical_url == creation_data["canonical_url"]
        assert isinstance(home_page.canonical_url, str)
        assert type(home_page.canonical_url) == type(creation_data["canonical_url"])

        assert home_page.main_title == creation_data["main_title"]
        assert isinstance(home_page.main_title, str)
        assert type(home_page.main_title) == type(creation_data["main_title"])

        assert home_page.main_description == creation_data["main_description"]
        assert isinstance(home_page.main_description, str)
        assert type(home_page.main_description) == type(
            creation_data["main_description"]
        )

    @pytest.mark.django_db(transaction=True)
    def test_discovery_url_must_be_unique(self, example_home_page, example_website):
        """Test that each HomePage have unique discovery_url"""

        website = example_website
        home_page_1 = example_home_page

        with pytest.raises(Exception):
            HomePage.objects.create(
                discovery_url="http://test.com/home",
                current_url="http://test.com/home",
                is_active=True,
                seo_title="Test Home",
                meta_description="Test Meta Home",
                canonical_url="http://test.com/home",
                parrent_website=website,
                main_title="Test Home",
                main_description="Sample home page...",
            )
        assert HomePage.objects.all().count() == 1

    def test_str_method_returns_proper_data(sel, example_home_page):
        """Test that __str__ for object is properly returning data."""

        home_page = example_home_page
        assert str(home_page) == home_page.main_title
