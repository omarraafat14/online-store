from rest_framework import serializers
from django.contrib.auth.models import User
from .models import Product, Cart, CartItem, Order, OrderItem


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email', 'password']
        extra_kwargs = {
            'email': {
                'style': {'input_type': 'email'}
            },
            'password': {
                'write_only': True,
                'style': {'input_type': 'password'}
            }
        }


class ProductSerializer(serializers.ModelSerializer):
    """Serializer for the Product model."""

    class Meta:
        model = Product
        fields = ['id', 'name', 'price']


class CartItemSerializer(serializers.ModelSerializer):
    """Serializer for the CartItem model."""

    product = ProductSerializer()

    class Meta:
        model = CartItem
        fields = ['id', 'product', 'quantity']
        extra_kwargs = {
            'quantity': {
                'min_value': 1,
                'max_value': 100,
            },
        }


class CartSerializer(serializers.ModelSerializer):
    """Serializer for the Cart model."""

    items = CartItemSerializer(many=True, read_only=True)

    class Meta:
        model = Cart
        fields = ['id', 'items']


class OrderItemSerializer(serializers.ModelSerializer):
    """Serializer for the OrderItem model."""

    product = ProductSerializer()

    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity']


class OrderSerializer(serializers.ModelSerializer):
    """Serializer for the Order model."""

    items = OrderItemSerializer(many=True, read_only=True)

    class Meta:
        model = Order
        fields = ['id', 'total', 'created_at', 'items']
