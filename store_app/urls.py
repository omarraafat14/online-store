from django.urls import path
from .views import (
    UserRegistrationView,
    UserLoginView,
    ProductListView,
    CartView,
    AddToCartView,
    CreateOrderView,
    OrderListView,
)

urlpatterns = [
    path('register/', UserRegistrationView.as_view(), name='register'),
    path('login/', UserLoginView.as_view(), name='login'),
    path('products/', ProductListView.as_view(), name='product-list'),
    path('cart/', CartView.as_view(), name='cart'),
    path('add-to-cart/', AddToCartView.as_view(), name='add-to-cart'),
    path('create-order/', CreateOrderView.as_view(), name='create-order'),
    path('orders/', OrderListView.as_view(), name='order-list'),
]
