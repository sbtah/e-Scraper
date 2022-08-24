from unicodedata import category
from django.test import TestCase
from categories.models import Category


class TestCategories(TestCase):
    """Test cases for Categories objects."""

    def test_category_is_created(self):
        """Test that new Category can be created in Database."""

        self.assertEqual(Category.objects.all().count(), 0)
        new_category = Category.objects.create(
            current_url="http://example.com/test-category",
            category_name="Test Category",
        )
        self.assertEqual(Category.objects.all().count(), 1)
        self.assertTrue(isinstance(new_category, Category))

    def test_category_str_representation(self):
        """Test that Category str method is working properly."""

        new_category = Category.objects.create(
            current_url="http://example.com/test-category",
            category_name="Test Category",
        )
        self.assertEqual(str(new_category), "Test Category")

    def test_category_can_be_add_to_other(self):
        """Test that Category object can be set as a child of other Category."""

        new_category_1 = Category.objects.create(
            current_url="http://example.com/test-category-1",
            category_name="Test Category 1",
        )
        new_category_2 = Category.objects.create(
            current_url="http://example.com/test-category-2",
            category_name="Test Category 2",
            parrent_category=new_category_1,
        )
        self.assertEqual(Category.objects.all().count(), 2)
        self.assertEqual(new_category_1.category_set.all().count(), 1)
        self.assertEqual(new_category_2.parrent_category.id, 1)
        self.assertEqual(new_category_1.category_set.all().count(), 1)
