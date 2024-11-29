from django.test import TestCase
from shop.models import Product, Customer, Purchase


class ModelsTestCase(TestCase):
    def setUp(self):
        # Создаем данные для тестов
        self.customer = Customer.objects.create(name="Иван Иванов", email="ivan@example.com")
        self.product = Product.objects.create(name="Тестовый товар", price=100)

    def test_customer_creation(self):
        """Тест создания клиента."""
        customer = Customer.objects.create(name="Мария Петрова", email="maria@example.com")
        self.assertEqual(customer.name, "Мария Петрова")
        self.assertEqual(customer.email, "maria@example.com")
        self.assertEqual(customer.total_purchases, 0)

    def test_product_creation(self):
        """Тест создания продукта."""
        product = Product.objects.create(name="Новый товар", price=200)
        self.assertEqual(product.name, "Новый товар")
        self.assertEqual(product.price, 200)

    def test_purchase_creation(self):
        """Тест создания покупки."""
        purchase = Purchase.objects.create(
            product=self.product,
            customer=self.customer,
            address="Ленина 10",
        )
        self.assertEqual(purchase.product, self.product)
        self.assertEqual(purchase.customer, self.customer)
        self.assertEqual(purchase.address, "Ленина 10")
        self.assertEqual(purchase.discount, 0)
        self.assertTrue(purchase.date)
