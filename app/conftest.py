import pytest
from projects.models.websites import Website
from projects.models.blogs import BlogPage


@pytest.fixture
def example_website():
    example_website = Website.objects.create(
        domain="test.com",
        module_name="teststore",
        scraper_class="TestStore",
    )
    return example_website


@pytest.fixture
def example_blog_page(example_website):
    website = example_website
    example_blog_page = BlogPage.objects.create(
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
    return example_blog_page
