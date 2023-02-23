# test_views.py 


from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from rest_framework import status
from rest_framework.test import APITestCase
from ..serializers import UserSerializer, ProductSerializer, CartItemSerializer, CartSerializer, OrderItemSerializer, OrderSerializer
from ..models import Product, Cart, CartItem, Order, OrderItem


class ProductTest(TestCase):
    def setUp(self):
        self.client = Client()
        self.product1 = Product.objects.create(name="Product1", price=10.00)
        self.product2 = Product.objects.create(name="Product2", price=20.00)

    def test_get_all_products(self):
        response = self.client.get(reverse('product-list'))
        products = Product.objects.all()
        serializer_data = ProductSerializer(products, many=True).data
        self.assertEqual(response.data, serializer_data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


class CartTest(APITestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.product1 = Product.objects.create(name="Product1", price=10.00)
        self.product2 = Product.objects.create(name="Product2", price=20.00)
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item1 = CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)
        self.cart_item2 = CartItem.objects.create(cart=self.cart, product=self.product2, quantity=3)
        self.client.login(username='testuser', password='testpass')

    def test_add_to_cart(self):
        url = reverse('add-to-cart')
        data = {'product_id': self.product1.id, 'quantity': 1}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        cart_items = CartItem.objects.filter(cart=self.cart)
        self.assertEqual(len(cart_items), 2)

    def test_view_cart(self):
        url = reverse('cart')
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['items']), 2)


class OrderTest(APITestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(username='testuser', password='testpass')
        self.product1 = Product.objects.create(name="Product1", price=10.00)
        self.product2 = Product.objects.create(name="Product2", price=20.00)
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item1 = CartItem.objects.create(cart=self.cart, product=self.product1, quantity=2)
        self.cart_item2 = CartItem.objects.create(cart=self.cart, product=self.product2, quantity=3)
        self.client.login(username='testuser', password='testpass')

    def test_create_order(self):
        url = reverse('create_order')
        data = {'cart_id': self.cart.id}
        response = self.client.post(url, data, format='json')
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

        order = Order.objects.get(user=self.user)
        self.assertEqual(order.total, 80.00)
