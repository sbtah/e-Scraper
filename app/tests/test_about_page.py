from django.test import TestCase
from projects.models.about import AboutPage
from projects.models.websites import Website


class TestAboutPage(TestCase):
    """Test cases for AboutPage object."""

    def setUp(self) -> None:

        self.website = Website.objects.create(
            domain="test.com",
            main_url="http://test.com/",
            module_name="test",
            scraper_class="Test",
        )

    def test_about_page_is_created(self):
        """Test that AboutPage object can be created."""

        objects_number_initial = AboutPage.objects.all().count()
        self.assertEqual(objects_number_initial, 0)
        page = AboutPage.objects.create(
            discovery_url="http://www.test.pl/",
            parrent_website=self.website,
            main_title="Test",
            main_description="Test Description",
            last_discovery="2022-11-22",
            last_scrape="2022-11-22",
        )
        objects_number_after = AboutPage.objects.all().count()
        self.assertEqual(objects_number_after, 1)
        self.assertTrue(isinstance(page, AboutPage))
