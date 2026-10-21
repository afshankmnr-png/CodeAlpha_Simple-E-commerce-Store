
from django.test import TestCase
from .models import Product


class ProductModelTest(TestCase):
    def test_product_creation(self):
        product = Product.objects.create(
            name="Headphones",
            description="Wireless headphones",
            price="999.00",
            stock=10,
        )

        self.assertEqual(product.name, "Headphones")
        self.assertEqual(product.price, 999)
        self.assertEqual(product.stock, 10)
