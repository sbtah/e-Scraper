from django.test import TestCase
from products.models import Product, ProductLocalData, ProductExtraField


class TestProducts(TestCase):
    """Test cases for Product objects."""

    def test_product_is_created(self):
        """Test that new Product can be created in Database."""

        self.assertEqual(Product.objects.all().count(), 0)
        new_product = Product.objects.create(
            current_url="http://example.com/test-product",
            product_name="Test Product",
        )
        self.assertEqual(Product.objects.all().count(), 1)
        self.assertTrue(isinstance(new_product, Product))

    def test_product_str_representation(self):
        """Test that Product str method is working properly."""

        new_product = Product.objects.create(
            current_url="http://example.com/test-product",
            product_name="Test Product",
        )
        self.assertEqual(str(new_product), "Test Product")


class TestProductLocalData(TestCase):
    """Test cases for ProductLocalData objects."""

    def test_product_local_data_is_created(self):
        """Test that new ProductLocalData object can be created and linked to parrent."""

        self.assertEqual(ProductLocalData.objects.all().count(), 0)
        new_product = Product.objects.create(
            current_url="http://example.com/test-product",
            product_name="Test Product",
        )
        new_product_local_data = ProductLocalData.objects.create(
            store_name="Test Store",
            product_availability=True,
            parrent_product=new_product,
        )
        self.assertTrue(isinstance(new_product_local_data, ProductLocalData))
        self.assertEqual(ProductLocalData.objects.all().count(), 1)

    def test_product_local_data_str_representation(self):
        """Test that ProductLocalData str method is working properly."""

        new_product = Product.objects.create(
            current_url="http://example.com/test-product",
            product_name="Test Product",
        )
        new_product_local_data = ProductLocalData.objects.create(
            store_name="Test Store",
            product_availability=True,
            parrent_product=new_product,
        )
        self.assertEqual(str(new_product_local_data), "Test Store")


class TestProductExtraField(TestCase):
    """Test cases for ProductExtraField objects."""

    def test_product_extra_field_is_created(self):
        """Test that new ProductExtraField object can be created and linked to parrent."""

        self.assertEqual(ProductExtraField.objects.all().count(), 0)
        new_product = Product.objects.create(
            current_url="http://example.com/test-product",
            product_name="Test Product",
        )
        new_product_extra_field = ProductExtraField.objects.create(
            name="Test Field",
            parrent_product=new_product,
        )
        self.assertTrue(isinstance(new_product_extra_field, ProductExtraField))
        self.assertEqual(ProductExtraField.objects.all().count(), 1)

    def test_product_extra_field_str_representation(self):
        """Test that ProductExtraField str method is working properly."""

        new_product = Product.objects.create(
            current_url="http://example.com/test-product",
            product_name="Test Product",
        )
        new_product_extra_field = ProductExtraField.objects.create(
            name="Test Field",
            parrent_product=new_product,
        )
        self.assertEqual(str(new_product_extra_field), "Test Field")
