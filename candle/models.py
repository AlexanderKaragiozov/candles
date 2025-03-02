import random
from symtable import Class

from django.db import models


class Gallery(models.Model):
    image = models.ImageField(upload_to='gallery/')


class Customer(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(unique=True)  # Ensure unique emails
    phone = models.CharField(max_length=15, unique=True)  # Ensure unique phone numbers
    city = models.CharField(max_length=100)
    address = models.TextField()
    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Candle(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    cent = models.CharField(max_length=50)
    price = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True, editable=False)
    promotion_price = models.FloatField(default=0)

    image = models.ImageField(upload_to='candles/')


    # Correct way to generate random reviews at save-time
    reviews = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.reviews == 0:  # Only set if reviews haven't been manually assigned
            self.reviews = random.randint(1, 70)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class CandleOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    candle = models.ForeignKey(Candle, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Support multiple candles in an order
    order_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Order by {self.customer.first_name} - {self.candle.name} (x{self.quantity})"

class Contacts(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    title = models.CharField(max_length=100)
    problem = models.TextField()
    def __str__(self):
        return {self.title}

