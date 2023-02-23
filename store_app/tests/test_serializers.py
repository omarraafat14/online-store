from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Product, Cart, CartItem, Order, OrderItem
from ..serializers import UserSerializer, ProductSerializer, CartItemSerializer, CartSerializer, OrderItemSerializer, OrderSerializer


class SerializerTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123',
            email='testuser@example.com'
        )
        self.product = Product.objects.create(
            name='Product 1',
            price=10.00
        )
        self.cart = Cart.objects.create(user=self.user)
        self.cart_item = CartItem.objects.create(
            cart=self.cart,
            product=self.product,
            quantity=2
        )
        self.order = Order.objects.create(
            user=self.user,
            total=20.00
        )
        self.order_item = OrderItem.objects.create(
            order=self.order,
            product=self.product,
            quantity=2
        )

    def test_user_serializer(self):
        serializer = UserSerializer(instance=self.user)
        self.assertEqual(serializer.data['username'], self.user.username)
        self.assertEqual(serializer.data['email'], self.user.email)

    def test_product_serializer(self):
        serializer = ProductSerializer(instance=self.product)
        self.assertEqual(serializer.data['name'], self.product.name)
        self.assertEqual(float(serializer.data['price']), self.product.price)

    def test_cart_item_serializer(self):
        serializer = CartItemSerializer(instance=self.cart_item)
        self.assertEqual(serializer.data['product']['name'], self.product.name)
        self.assertEqual(serializer.data['quantity'], self.cart_item.quantity)

    def test_cart_serializer(self):
        serializer = CartSerializer(instance=self.cart)
        self.assertEqual(serializer.data['id'], self.cart.id)
        self.assertEqual(serializer.data['items'][0]['product']['name'], self.product.name)
        self.assertEqual(serializer.data['items'][0]['quantity'], self.cart_item.quantity)

    def test_order_item_serializer(self):
        serializer = OrderItemSerializer(instance=self.order_item)
        self.assertEqual(serializer.data['product']['name'], self.product.name)
        self.assertEqual(serializer.data['quantity'], self.order_item.quantity)

    def test_order_serializer(self):
        serializer = OrderSerializer(instance=self.order)
        self.assertEqual(serializer.data['id'], self.order.id)
        self.assertEqual(float(serializer.data['total']), self.order.total)
        self.assertEqual(serializer.data['items'][0]['product']['name'], self.product.name)
        self.assertEqual(serializer.data['items'][0]['quantity'], self.order_item.quantity)
