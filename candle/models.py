import random
from datetime import timedelta

from django.utils.timezone import now

from candle.spreadsheet import confirm_order
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
        return f"{self.first_name} {self.last_name}, тел.{self.phone}"


class Candle(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    cent = models.CharField(max_length=50)
    price = models.FloatField()
    date_added = models.DateTimeField(auto_now_add=True, editable=False)
    promotion_price = models.FloatField(default=0)
    quantity = models.PositiveIntegerField(default=0)  # Added quantity field

    image = models.ImageField(upload_to='candles/')
    image_2 = models.ImageField(upload_to='candles/', blank=True, null=True)  # Additional image
    image_3 = models.ImageField(upload_to='candles/', blank=True, null=True)  # Additional image
    image_4 = models.ImageField(upload_to='candles/', blank=True, null=True)  # Additional image


    # Correct way to generate random reviews at save-time
    reviews = models.IntegerField(default=0)

    def save(self, *args, **kwargs):
        if self.reviews == 0:  # Only set if reviews haven't been manually assigned
            self.reviews = random.randint(1, 70)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

def get_default_deadline():
    return now() + timedelta(hours=24)
class CandleOrder(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    candle = models.ForeignKey(Candle, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)  # Support multiple candles in an order
    order_date = models.DateTimeField(auto_now_add=True)
    confirmed = models.BooleanField(default=False)
    deadline = models.DateTimeField(default=get_default_deadline())

    def __str__(self):
        return f"Order by {self.customer.first_name} - {self.candle.name} (x{self.quantity})"

    def save(self, *args, **kwargs):
        if self.pk:  # Ensure the order exists
            old_order = CandleOrder.objects.get(pk=self.pk)
            if not old_order.confirmed and self.confirmed:  # If confirmed changed from False to True
                confirm_order(self.id)

        super().save(*args, **kwargs)  # Save the model
class Contacts(models.Model):
    email = models.EmailField()
    phone = models.CharField(max_length=15)
    title = models.CharField(max_length=100)
    problem = models.TextField()
    def __str__(self):
        return {self.title}

