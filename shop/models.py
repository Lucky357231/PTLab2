from django.db import models


class Customer(models.Model):
    name = models.CharField(max_length=200, unique=True)
    email = models.EmailField(unique=True)
    total_purchases = models.PositiveIntegerField(default=0)


class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.PositiveIntegerField()


class Purchase(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    address = models.CharField(max_length=200)
    date = models.DateTimeField(auto_now_add=True)
    discount = models.PositiveIntegerField(default=0)