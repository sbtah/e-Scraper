import pytest
from projects.models.webpages import WebPage
from projects.models.blogs import BlogPage
from projects.models.articles import BlogArticlePage


pytestmark = pytest.mark.django_db


class TestBlogArticlePageModel:
    """Test cases for BlogArticlePage object."""

    def test_about_article_page_can_be_created(
        self,
        example_website,
        example_blog_page,
        blog_article_page_create_test_data,
    ):
        """Test that BlogArticlePage object is created with proper values and types."""

        website = example_website
        blog_page = example_blog_page
        creation_data = blog_article_page_create_test_data

        assert BlogArticlePage.objects.all().count() == 0
        blog_article_page = BlogArticlePage.objects.create(
            discovery_url=creation_data["discovery_url"],
            current_url=creation_data["current_url"],
            is_active=creation_data["is_active"],
            seo_title=creation_data["seo_title"],
            meta_description=creation_data["meta_description"],
            canonical_url=creation_data["canonical_url"],
            parrent_website=website,
            blog_title=creation_data["blog_title"],
            blog_author=creation_data["blog_author"],
            blog_tags=creation_data["blog_tags"],
            parrent_blog_page=blog_page,
        )
        assert BlogArticlePage.objects.all().count() == 1
        assert blog_article_page.parrent_website.domain == "test.com"
        assert blog_article_page.parrent_blog_page.main_title == "Our Test Blogs"
        assert isinstance(blog_article_page, BlogArticlePage)
        assert isinstance(blog_article_page, WebPage)

        assert blog_article_page.discovery_url == creation_data["discovery_url"]
        assert isinstance(blog_article_page.discovery_url, str)
        assert type(blog_article_page.discovery_url) == type(
            creation_data["discovery_url"]
        )

        assert blog_article_page.current_url == creation_data["current_url"]
        assert isinstance(blog_article_page.current_url, str)
        assert type(blog_article_page.current_url) == type(creation_data["current_url"])

        assert blog_article_page.is_active == creation_data["is_active"]
        assert isinstance(blog_article_page.is_active, bool)
        assert type(blog_article_page.is_active) == type(creation_data["is_active"])

        assert blog_article_page.seo_title == creation_data["seo_title"]
        assert isinstance(blog_article_page.seo_title, str)
        assert type(blog_article_page.seo_title) == type(creation_data["seo_title"])

        assert blog_article_page.meta_description == creation_data["meta_description"]
        assert isinstance(blog_article_page.meta_description, str)
        assert type(blog_article_page.meta_description) == type(
            creation_data["meta_description"]
        )

        assert blog_article_page.canonical_url == creation_data["canonical_url"]
        assert isinstance(blog_article_page.canonical_url, str)
        assert type(blog_article_page.canonical_url) == type(
            creation_data["canonical_url"]
        )

        assert blog_article_page.blog_title == creation_data["blog_title"]
        assert isinstance(blog_article_page.blog_title, str)
        assert type(blog_article_page.blog_title) == type(creation_data["blog_title"])

        assert blog_article_page.blog_author == creation_data["blog_author"]
        assert isinstance(blog_article_page.blog_author, str)
        assert type(blog_article_page.blog_author) == type(creation_data["blog_author"])

        assert blog_article_page.blog_tags == creation_data["blog_tags"]
        assert isinstance(blog_article_page.blog_tags, list)
        assert type(blog_article_page.blog_tags) == type(creation_data["blog_tags"])

    @pytest.mark.django_db(transaction=True)
    def test_blog_title_must_be_unique(
        self,
        example_website,
        example_blog_page,
        example_blog_article_page,
    ):
        """Test that each BlogArticlePage can be saved with unique blog_title."""

        website = example_website
        blog_page = example_blog_page
        blog_article_page_1 = example_blog_article_page

        with pytest.raises(Exception):
            BlogArticlePage.objects.create(
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

    def test_str_method_returns_proper_data(sel, example_blog_article_page):
        """Test that __str__ for object is properly returning data."""

        blog_article_page = example_blog_article_page
        assert str(blog_article_page) == blog_article_page.blog_title
