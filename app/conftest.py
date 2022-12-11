import pytest
from projects.models.websites import Website
from projects.models.blogs import BlogPage
from projects.models.about import AboutPage


@pytest.fixture
def website_create_test_data():
    return {
        "domain": "test.com",
        "is_monitored": True,
        "module_name": "teststore",
        "scraper_class": "TestStore",
    }


@pytest.fixture
def example_website():
    example_website = Website.objects.create(
        domain="test.com",
        is_monitored=True,
        module_name="teststore",
        scraper_class="TestStore",
    )
    return example_website


@pytest.fixture
def blog_page_create_test_data():
    return {
        "discovery_url": "http://test.com/",
        "current_url": "http://test.com/",
        "is_active": True,
        "seo_title": "TestWeb",
        "meta_description": "Test Meta",
        "canonical_url": "http://test.com/",
        "main_title": "Our Test Blogs",
        "main_description": "Test...",
    }


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


@pytest.fixture
def about_page_create_test_data():
    return {
        "discovery_url": "http://test.com/about",
        "current_url": "http://test.com/about",
        "is_active": True,
        "seo_title": "Test About",
        "meta_description": "Test Meta",
        "canonical_url": "http://test.com/about",
        "main_title": "Test About",
        "main_description": "Sample about us text...",
    }


@pytest.fixture
def example_about_page(example_website):
    website = example_website
    example_about_page = AboutPage.objects.create(
        discovery_url="http://test.com/about",
        current_url="http://test.com/about",
        is_active=True,
        seo_title="Test About",
        meta_description="Test Meta",
        canonical_url="http://test.com/about",
        parrent_website=website,
        main_title="Test About",
        main_description="Sample about us text...",
    )
    return example_about_page
