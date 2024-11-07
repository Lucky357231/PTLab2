from django.test import TestCase
from shop.models import Product, Purchase, Customer
from datetime import datetime


class ProductTestCase(TestCase):
    def setUp(self):
        Product.objects.create(name="Стол", price=2000)
        Product.objects.create(name="Стул", price=1000)

    def test_correctness_types(self):
        self.assertIsInstance(Product.objects.get(name="Стол").name, str)
        self.assertIsInstance(Product.objects.get(name="Стол").price, int)
        self.assertIsInstance(Product.objects.get(name="Стул").name, str)
        self.assertIsInstance(Product.objects.get(name="Стул").price, int)

    def test_correctness_data(self):
        self.assertTrue(Product.objects.get(name="Стол").price == 2000)
        self.assertTrue(Product.objects.get(name="Стул").price == 1000)


class CustomerTestCase(TestCase):
    def setUp(self):
        Customer.objects.create(name="Иван Иванов", email="ivan@example.com", total_purchases=11)

    def test_correctness_types(self):
        customer = Customer.objects.get(name="Иван Иванов")
        self.assertIsInstance(customer.name, str)
        self.assertIsInstance(customer.email, str)
        self.assertIsInstance(customer.total_purchases, int)

    def test_correctness_data(self):
        customer = Customer.objects.get(name="Иван Иванов")
        self.assertEqual(customer.email, "ivan@example.com")
        self.assertEqual(customer.total_purchases, 11)


class PurchaseTestCase(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Стол", price=2000)
        self.customer = Customer.objects.create(
            name="Ivanov",
            email="ivanov@example.com",
            total_purchases=11
        )

    def test_receipt_data(self):
        """Проверка расчета скидки и итоговой цены."""
        purchase = Purchase.objects.create(
            product=self.product,
            customer=self.customer,
            address="Ленина 3"
        )
        purchase.apply_discount()  # Применяем скидку
        discounted_price = self.product.price * (1 - purchase.discount / 100)

        # Проверяем, что скидка 15% применена и цена верная
        self.assertEqual(discounted_price, 1700)  # Цена со скидкой 15%