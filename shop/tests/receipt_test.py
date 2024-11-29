from django.test import TestCase
from django.urls import reverse
from shop.models import Product, Customer, Purchase


class ReceiptTemplateTestCase(TestCase):
    def setUp(self):
        """Создаем тестовые данные для страницы чека."""
        self.customer = Customer.objects.create(name="Иван Иванов", email="ivanov@example.com", total_purchases=3)
        self.product = Product.objects.create(name="Продукт 1", price=100)
        self.purchase = Purchase.objects.create(
            product=self.product,
            customer=self.customer,
            address="Ленина 10",
            discount=5
        )

    def test_receipt_content(self):
        """Тест содержимого страницы чека."""
        response = self.client.get(reverse('index'))  # Замените URL на соответствующий, если нужен другой маршрут
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Чек")
        self.assertContains(response, "Иван Иванов")
        self.assertContains(response, "Ленина 10")
        self.assertContains(response, "5%")
        self.assertContains(response, "100 руб.")
        self.assertContains(response, "Спасибо за покупку!")

    def test_purchase_date_format(self):
        """Тест формата даты покупки на странице."""
        response = self.client.get(reverse('index'))
        self.assertContains(response, self.purchase.date.strftime("%d-%m-%Y %H:%M"))
