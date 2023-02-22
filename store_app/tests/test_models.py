from django.test import TestCase
from store_app.models import Product


# Create your tests here.
class ProductTest(TestCase):

    def test_get_product(self):
        product = Product.objects.create(
            name = 'Iphone 11',
            price = 899.00
        )
        productstr = product.get_product()
        self.assertEqual(productstr, 'Iphone 11')