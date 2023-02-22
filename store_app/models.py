from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Product(models.Model):
    """Product model which has a name and a price."""
    name = models.CharField(max_length=255 , db_index=True)
    price = models.DecimalField(max_digits=6 , decimal_places=2)

    def __str__(self):
        return self.name


class Cart(models.Model):
    """represents a Cart which belongs to a user"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)


class CartItem(models.Model):
    """instances of a Cart model"""
    cart = models.ForeignKey(Cart,related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = ('product', 'cart')


class Order(models.Model):
    """represents an order made by a user, and has a total and a creation date"""
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    total = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    """Objects of the Order Model"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField(default=1)

    class Meta:
        unique_together = ('order', 'product')