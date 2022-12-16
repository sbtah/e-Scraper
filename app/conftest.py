import pytest
from projects.models.websites import Website
from projects.models.contact import ContactPage
from projects.models.blogs import BlogPage
from projects.models.home import HomePage
from projects.models.articles import BlogArticlePage
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


@pytest.fixture
def home_page_create_test_data():
    return {
        "discovery_url": "http://test.com/home",
        "current_url": "http://test.com/home",
        "is_active": True,
        "seo_title": "Test Home",
        "meta_description": "Test Meta Home",
        "canonical_url": "http://test.com/home",
        "main_title": "Test Home",
        "main_description": "Sample home page...",
    }


@pytest.fixture
def example_home_page(example_website):
    website = example_website
    example_home_page = HomePage.objects.create(
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
    return example_home_page


@pytest.fixture
def blog_article_page_create_test_data():
    return {
        "discovery_url": "http://test.com/blog/test",
        "current_url": "http://test.com/blog/test",
        "is_active": True,
        "seo_title": "Hello, test article!",
        "meta_description": "Test Article Meta ...",
        "canonical_url": "http://test.com/blog/test",
        "blog_title": "Hello, test article!",
        "blog_author": "Test Author",
        "blog_tags": ["Test1", "Test2"],
    }


@pytest.fixture
def example_blog_article_page(example_website, example_blog_page):

    website = example_website
    blog_page = example_blog_page

    example_blog_article_page = BlogArticlePage.objects.create(
        discovery_url="http://test.com/blog/test",
        current_url="http://test.com/blog/test",
        is_active=True,
        seo_title="Hello, test article!",
        meta_description="Test Article Meta ...",
        canonical_url="http://test.com/blog/test",
        parrent_website=website,
        blog_title="Hello, test article!",
        blog_author="Test Author",
        blog_tags=["Test1", "Test2"],
        parrent_blog_page=blog_page,
    )
    return example_blog_article_page


@pytest.fixture
def contact_page_create_test_data():
    return {
        "discovery_url": "http://test.com/contact",
        "current_url": "http://test.com/contact",
        "is_active": True,
        "seo_title": "Contact Page",
        "meta_description": "Test Contact Meta ...",
        "canonical_url": "http://test.com/contact",
        "company_name": "Test Company",
        "company_address": "Test Address",
        "company_phone": "111-111-111",
        "company_email_address": "test@company.com",
    }


@pytest.fixture
def example_contact_page(example_website):
    website = example_website
    example_contact_page = ContactPage.objects.create(
        discovery_url="http://test.com/contact",
        current_url="http://test.com/contact",
        is_active=True,
        seo_title="Contact Page",
        meta_description="Test Contact Meta ...",
        canonical_url="http://test.com/contact",
        parrent_website=website,
        company_name="Test Company",
        company_address="Test Address",
        company_phone="111-111-111",
        company_email_address="test@company.com",
    )
    return example_contact_page
