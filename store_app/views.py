from django.contrib.auth import authenticate, login
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import BasicAuthentication
from .models import Product, Cart, CartItem, Order, OrderItem
from .serializers import (
    UserSerializer,
    ProductSerializer,
    CartItemSerializer,
    CartSerializer,
    OrderSerializer
)


class UserRegistrationView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Hash the password before saving
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        serializer = UserSerializer(user)
        return Response(serializer.data)


class UserLoginView(generics.GenericAPIView):
    serializer_class = UserSerializer

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        # Authenticate the user
        user = authenticate(request, username=username, password=password)
        if user:
            login(request, user)
            serializer = UserSerializer(user)
            return Response(serializer.data)
        return Response({'error': 'Invalid credentials'})


class ProductListView(generics.ListAPIView):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer

    ordering_fields = ['price']
    search_fields = ['name']


class CartView(generics.RetrieveUpdateAPIView):
    """represent a single model instance."""
    serializer_class = CartSerializer
    # permission_classes = [IsAuthenticated]

    def get_object(self):
        """Returns an object instance that should be used for detail views."""
        cart, created = Cart.objects.get_or_create(user=self.request.user)
        return cart


class AddToCartView(generics.CreateAPIView):
    serializer_class = CartItemSerializer
    authentication_classes = [BasicAuthentication]
    # permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):
        product_id = request.data.get('product_id')
        quantity = request.data.get('quantity', 1)
        product = get_object_or_404(Product, id=product_id)
        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)
        cart_item.quantity += int(quantity)
        cart_item.save()
        serializer = CartItemSerializer(cart_item)
        return Response(serializer.data)


class CreateOrderView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]
    authentication_classes = [BasicAuthentication]

    def post(self, request, *args, **kwargs):
        cart = get_object_or_404(Cart, user=request.user)
        order = Order(user=request.user, total=0)
        order.save()
        order_items = []
        total = 0
        for cart_item in cart.items.all():
            order_item = OrderItem(
                order=order,
                product=cart_item.product,
                quantity=cart_item.quantity
            )
            order_items.append(order_item)
            total += order_item.product.price * order_item.quantity
        order.total = total
        order.save()
        OrderItem.objects.bulk_create(order_items)  # creates multiple objects of the OrderItem in a snigle query
        cart.items.all().delete()
        serializer = OrderSerializer(order)
        return Response(serializer.data)


class OrderListView(generics.ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        return Order.objects.filter(user=self.request.user)
