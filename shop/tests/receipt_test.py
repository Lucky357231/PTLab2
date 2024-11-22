from django.test import TestCase
from django.urls import reverse
from shop.models import Customer, Product, Purchase


class ReceiptViewTests(TestCase):
    def setUp(self):
        # Создаем тестовые данные
        self.customer = Customer.objects.create(name="Иван Иванов", email="ivanov@example.com", total_purchases=12)
        self.product = Product.objects.create(name="Стол", price=2000)
        self.purchase = Purchase.objects.create(
            customer=self.customer,
            product=self.product,
            address="ул. Ленина, д.3",
            price=self.product.price * 0.85,  # Учитывая скидку 15%
        )

    def test_receipt_view_status_code(self):
        # Тестируем, что страница чека возвращает статус 200
        response = self.client.get(reverse('receipt', kwargs={'pk': self.purchase.id}))
        self.assertEqual(response.status_code, 200)

    def test_receipt_context(self):
        # Тестируем, что контекст содержит ожидаемые данные
        response = self.client.get(reverse('receipt', kwargs={'pk': self.purchase.id}))
        self.assertEqual(response.context['customer'], self.customer)
        self.assertEqual(response.context['product'], self.product)
        self.assertEqual(response.context['original_price'], self.product.price)
        self.assertEqual(response.context['discount'], 15)
        self.assertEqual(response.context['discounted_price'], self.purchase.price)
        self.assertEqual(response.context['total_purchases'], self.customer.total_purchases)

    def test_receipt_html_content(self):
        # Тестируем, что HTML-контент содержит правильные данные
        response = self.client.get(reverse('receipt', kwargs={'pk': self.purchase.id}))

        self.assertContains(response, "Чек")
        self.assertContains(response, "Иван Иванов")
        self.assertContains(response, "ivanov@example.com")
        self.assertContains(response, "12")
        self.assertContains(response, "Стол")
        self.assertContains(response, "2000 руб.")
        self.assertContains(response, "15%")
        self.assertContains(response, "1700 руб.")  # Итоговая цена со скидкой
        self.assertContains(response, "Спасибо за покупку!")

    def test_return_link(self):
        # Проверяем ссылку для возврата к покупкам
        response = self.client.get(reverse('receipt', kwargs={'pk': self.purchase.id}))
        self.assertContains(response, 'href="{}"'.format(reverse('index')))
        self.assertContains(response, "Вернуться к покупкам")
