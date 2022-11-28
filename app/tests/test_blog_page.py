from django.test import TestCase
from projects.models.blogs import BlogPage
from projects.models.websites import Website


class TestBlogPage(TestCase):
    """Test cases for BlogPage object."""

    def setUp(self):

        self.website = Website.objects.create(
            domain="test.com",
            main_url="http://test.com/",
            module_name="test",
            scraper_class="Test",
        )

    def test_blog_page_is_created(self):
        """Test that BlogPage can be created."""

        objects_number_inital = BlogPage.objects.all().count()
        self.assertEqual(objects_number_inital, 0)

        page = BlogPage.objects.create(
            discovery_url="http://test.pl",
            parrent_website=self.website,
            blog_title="Test title",
            blog_author="Author",
            blog_tags=["funny", "test"],
            date_published="2022-11-22",
            last_discovery="2022-11-22",
            last_scrape="2022-11-22",
        )
        objects_number_after = BlogPage.objects.all().count()
        self.assertEqual(objects_number_after, 1)
        self.assertTrue(isinstance(page, BlogPage))

    def test_str_method(self):
        """Test that BlogPage object generates proper __str__."""

        page = BlogPage.objects.create(
            discovery_url="http://test.pl",
            parrent_website=self.website,
            blog_title="Test title",
            blog_author="Author",
            blog_tags=["funny", "test"],
            date_published="2022-11-22",
            last_discovery="2022-11-22",
            last_scrape="2022-11-22",
        )
        self.assertEqual(page.blog_title, str(page))
