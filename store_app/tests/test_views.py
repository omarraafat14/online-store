from django.test import TestCase, Client
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.models import User
from ..models import Product, Cart, CartItem, Order, OrderItem
from ..serializers import (
    UserSerializer,
    ProductSerializer,
    CartItemSerializer,
    CartSerializer,
    OrderSerializer
)

class UserRegistrationViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('register')
        self.valid_payload = {
            "username": "testuser",
            "email": "useremail22@example.com",
            "password": "testpassword"
        }
        self.invalid_payload = {
            'username': '',
            'email': 'invalidemail',
            'password': 'testpassword'
        }

    def test_valid_registration(self):
        response = self.client.post(
            self.url,
            data=self.valid_payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_registration(self):
        response = self.client.post(
            self.url,
            data=self.invalid_payload,
            content_type='application/json'
        )
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


class UserLoginViewTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('login')
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@gmail.com',
            password='testpassword'
        )

    def test_valid_login(self):
        response = self.client.post(
            self.url,
            data={
                'username': 'testuser',
                'password': 'testpassword'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_invalid_login(self):
        response = self.client.post(
            self.url,
            data={
                'username': 'testuser',
                'password': 'invalidpassword'
            },
            format='json'
        )
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ProductListViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.url = reverse('products-list')
        self.product1 = Product.objects.create(
            name='Test Product 1',
            price=10.0
        )
        self.product2 = Product.objects.create(
            name='Test Product 2',
            price=20.0
        )

    def test_product_list_view(self):
        response = self.client.get(self.url)
        products = Product.objects.all()
        serializer = ProductSerializer(products, many=True)
        self.assertEqual(response.data, serializer.data)


class CartViewTestCase(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = User.objects.create_user(
            username='testuser',
            email='testuser@gmail.com',
            password='testpassword'
        )
        refresh = RefreshToken.for_user(self.user)
        self.client.credentials(HTTP_AUTHORIZATION=f'Bearer {refresh.access_token}')
        self.cart = Cart.objects.create(user=self.user)

    def test_cart_view(self):
        response = self.client.get(reverse('cart-detail'))
        serializer = CartSerializer(self.cart)
        self.assertEqual(response.data, serializer.data)
