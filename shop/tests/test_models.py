from django.test import TestCase
from shop.models import Product, Purchase
from datetime import datetime

class ProductTestCase(TestCase):
    def setUp(self):
        # Создаем тестовые продукты с целым числом в поле 'price'
        Product.objects.create(name="book", price=740)
        Product.objects.create(name="pencil", price=50)

    def test_correctness_types(self):
        # Проверка типов данных полей модели Product
        self.assertIsInstance(Product.objects.get(name="book").name, str)
        self.assertIsInstance(Product.objects.get(name="book").price, int)
        self.assertIsInstance(Product.objects.get(name="pencil").name, str)
        self.assertIsInstance(Product.objects.get(name="pencil").price, int)

    def test_correctness_data(self):
        # Проверка корректности данных полей модели Product
        self.assertEqual(Product.objects.get(name="book").price, 740)
        self.assertEqual(Product.objects.get(name="pencil").price, 50)


class PurchaseTestCase(TestCase):
    def setUp(self):
        # Создаем тестовый продукт и покупку с новыми полями customer_name и customer_email
        self.product_book = Product.objects.create(name="book", price=740)
        self.datetime = datetime.now()
        Purchase.objects.create(
            product=self.product_book,
            customer_name="Ivanov",
            customer_email="ivanov@example.com",
            address="Svetlaya St."
        )

    def test_correctness_types(self):
        # Проверка типов данных полей модели Purchase
        purchase = Purchase.objects.get(product=self.product_book)
        self.assertIsInstance(purchase.customer_name, str)
        self.assertIsInstance(purchase.customer_email, str)
        self.assertIsInstance(purchase.address, str)
        self.assertIsInstance(purchase.date, datetime)

    def test_correctness_data(self):
        # Проверка корректности данных полей модели Purchase
        purchase = Purchase.objects.get(product=self.product_book)
        self.assertEqual(purchase.customer_name, "Ivanov")
        self.assertEqual(purchase.customer_email, "ivanov@example.com")
        self.assertEqual(purchase.address, "Svetlaya St.")
        self.assertEqual(purchase.date.replace(microsecond=0), self.datetime.replace(microsecond=0))
