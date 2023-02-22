from django.test import TestCase
import json
from store_app.models import Product
from store_app.serializers import ProductSerializer
from store_app.views import ProductListView


# Create your tests here.
class ProductListViewTest(TestCase):

    def test_getall(self):
        # Get all menu items
        product = Product.objects.all()
        serialized_product = ProductSerializer(product, many=True)
        response = self.client.get('/api/products/')
        response_data = json.loads(response.content)

        # Make sure the serialized data equals the response
        self.assertEqual(serialized_product.data, response_data)
        self.assertEqual(response.status_code, 200)