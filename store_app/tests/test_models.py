from decimal import Decimal
from django.test import TestCase
from django.contrib.auth.models import User
from ..models import Product, Cart, CartItem, Order, OrderItem


class ProductTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Test Product", price=Decimal('10.00'))

    def test_product_str(self):
        self.assertEqual(str(self.product), "Test Product")


class CartTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpass')
        self.cart = Cart.objects.create(user=self.user)

    def test_cart_user(self):
        self.assertEqual(self.cart.user, self.user)


class CartItemTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpass')
        self.cart = Cart.objects.create(user=self.user)
        self.product = Product.objects.create(name="Test Product", price=Decimal('10.00'))
        self.cart_item = CartItem.objects.create(cart=self.cart, product=self.product, quantity=2)

    def test_cart_item_quantity(self):
        self.assertEqual(self.cart_item.quantity, 2)

    def test_cart_item_product(self):
        self.assertEqual(self.cart_item.product, self.product)


class OrderTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpass')
        self.order = Order.objects.create(user=self.user, total=Decimal('50.00'))

    def test_order_user(self):
        self.assertEqual(self.order.user, self.user)

    def test_order_total(self):
        self.assertEqual(self.order.total, Decimal('50.00'))


class OrderItemTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='testpass')
        self.product = Product.objects.create(name="Test Product", price=Decimal('10.00'))
        self.order = Order.objects.create(user=self.user, total=Decimal('50.00'))
        self.order_item = OrderItem.objects.create(order=self.order, product=self.product, quantity=3)

    def test_order_item_quantity(self):
        self.assertEqual(self.order_item.quantity, 3)

    def test_order_item_product(self):
        self.assertEqual(self.order_item.product, self.product)
