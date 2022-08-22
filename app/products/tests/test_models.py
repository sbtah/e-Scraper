from django.test import TestCase
from products.models import Product


class TestProducts(TestCase):
    """Test cases for Product objects."""

    def test_product_is_created(self):
        """Test that new Product can be created in Database"""

        self.assertEqual(Product.objects.all().count(), 0)
        new_product = Product.objects.create(
            current_url="http://example.com/test-product",
            product_name="Test Product",
        )
        self.assertEqual(Product.objects.all().count(), 1)
        self.assertTrue(isinstance(new_product, Product))
