from django.db import models
from django.contrib.auth.models import User


class Orders(models.Model):
    user=models.ForeignKey(User, on_delete=models.CASCADE)

    order_type_choices = [
        ('LIMIT', 'LIMIT'),
        ('MARKET', 'MARKET'),
    ]
    side_choices = [
        ('BUY', 'buy'),
        ('SELL', 'sell')
    ]

    symbol = models.CharField(max_length=20)
    order_type = models.CharField(max_length=10, choices=order_type_choices)
    side = models.CharField(max_length=10, choices=side_choices)
    price = models.DecimalField(max_digits=20, decimal_places=10)
    quantity = models.DecimalField(max_digits=20, decimal_places=10)
    created_at = models.DateTimeField(auto_now_add=True)

    order_id = models.CharField(max_length=100, unique=True)
    status = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.user.username} - {self.symbol} - {self.side} - {self.order_type}"

    