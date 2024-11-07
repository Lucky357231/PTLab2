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

    def apply_discount(self):
        """Расчет скидки на основе количества покупок клиента."""
        if self.customer.total_purchases > 10:
            self.discount = 15
        elif self.customer.total_purchases >= 5:
            self.discount = 10
        else:
            self.discount = 5
        self.save()

    def discounted_price(self):
        """Возвращает цену товара после применения скидки."""
        return int(self.product.price * (1 - self.discount / 100))

    def __str__(self):
        return f"{self.customer.name} - {self.product.name} ({self.discount}% скидка)"
