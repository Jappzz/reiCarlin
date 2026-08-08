from django.db import models
from django.conf import settings

from reiCarlin.produtos.models import Product

class Order(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODELS, on_delete=models.CASCADE, related_name="orders")
    status = models.CharField(max_length=20, default="pending")
    created_at = models.DateTimeField(auto_now_add=True)


class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name="order")
    product = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    