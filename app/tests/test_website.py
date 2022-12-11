import pytest
from projects.models.websites import Website


pytestmark = pytest.mark.django_db


class TestWebsiteModel:
    """Test cases for Website object."""

    def test_website_can_be_created(self, website_create_test_data):
        """Test that Website object is created with proper values and type."""

        creation_data = website_create_test_data

        assert Website.objects.all().count() == 0
        website = Website.objects.create(
            domain=creation_data["domain"],
            is_monitored=creation_data["is_monitored"],
            module_name=creation_data["module_name"],
            scraper_class=creation_data["scraper_class"],
        )
        assert Website.objects.all().count() == 1
        assert isinstance(website, Website)

        assert website.domain == creation_data["domain"]
        assert isinstance(website.domain, str)
        assert type(website.domain) == type(creation_data["domain"])

        assert website.is_monitored == creation_data["is_monitored"]
        assert isinstance(website.is_monitored, bool)
        assert type(website.is_monitored) == type(creation_data["is_monitored"])

        assert website.module_name == creation_data["module_name"]
        assert isinstance(website.module_name, str)
        assert type(website.module_name) == type(creation_data["module_name"])

        assert website.scraper_class == creation_data["scraper_class"]
        assert isinstance(website.scraper_class, str)
        assert type(website.scraper_class) == type(creation_data["scraper_class"])

    @pytest.mark.django_db(transaction=True)
    def test_domain_module_name_scraper_class_must_be_unique(
        self,
        example_website,
        website_create_test_data,
    ):
        """
        Test that Website won't be created,
            if there is already a Website object with same value for:
            - domain,
            - module_name,
            - scraper_class.
        """

        creation_data = website_create_test_data
        website_1 = example_website

        with pytest.raises(Exception):
            Website.objects.create(
                domain=creation_data["domain"],
                is_monitored=True,
                module_name="teststore1",
                scraper_class="TestStore1",
            )

        with pytest.raises(Exception):
            Website.objects.create(
                domain="test2.com",
                is_monitored=True,
                module_name=creation_data["module_name"],
                scraper_class="TestStore2",
            )

        with pytest.raises(Exception):
            Website.objects.create(
                domain="test3.com",
                is_monitored=True,
                module_name="teststore3",
                scraper_class=creation_data["scraper_class"],
            )

        assert Website.objects.all().count() == 1

    def test_str_method_returns_proper_data(sel, example_website):
        """Test that __str__ for object is properly returning data."""

        website = example_website
        assert str(website) == website.domain
