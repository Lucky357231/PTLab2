from django.test import TestCase, RequestFactory
from django.urls import reverse
from shop.models import Product, Customer, Purchase
from shop.views import PurchaseCreate, index


class IndexViewTestCase(TestCase):
    def setUp(self):
        """Создаем тестовые данные для главной страницы."""
        Product.objects.create(name="Продукт 1", price=100)
        Product.objects.create(name="Продукт 2", price=200)

    def test_index_view(self):
        """Тест отображения главной страницы."""
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Просмотрите наши товары")
        self.assertContains(response, "Продукт 1")
        self.assertContains(response, "Продукт 2")


class PurchaseCreateViewTestCase(TestCase):
    def setUp(self):
        """Создаем тестовые данные для представления покупки."""
        self.factory = RequestFactory()
        self.product = Product.objects.create(name="Продукт 1", price=100)
        self.customer = Customer.objects.create(name="Иван Иванов", email="ivanov@example.com", total_purchases=5)

    def test_get_context_data(self):
        """Тест контекста представления."""
        url = reverse('buy', kwargs={'product_id': self.product.id})
        request = self.factory.get(url)

        # Создаем экземпляр представления
        view = PurchaseCreate()
        view.request = request
        view.kwargs = {'product_id': self.product.id}

        # Устанавливаем объект формы, чтобы избежать отсутствия `object`
        view.object = None

        # Проверяем контекст
        context = view.get_context_data()
        self.assertIn('product', context)
        self.assertEqual(context['product'], self.product)

    def test_form_valid_creates_purchase(self):
        """Тест создания покупки через form_valid."""
        form_data = {"address": "Ленина 10", "customer_name": "Иван Иванов"}
        url = reverse('buy', kwargs={'product_id': self.product.id})
        request = self.factory.post(url, form_data)

        # Создаем экземпляр представления
        view = PurchaseCreate.as_view()

        # Вызываем представление
        response = view(request, product_id=self.product.id)
        self.assertEqual(response.status_code, 200)

        # Проверяем, что покупка была создана
        purchase = Purchase.objects.get(product=self.product, customer=self.customer)
        self.assertEqual(purchase.address, "Ленина 10")
        self.assertEqual(purchase.discount, 10)

    def test_discount_logic(self):
        """Тест расчета скидки."""
        self.customer.total_purchases = 12
        self.customer.save()

        form_data = {"address": "Ленина 10", "customer_name": "Иван Иванов"}
        url = reverse('buy', kwargs={'product_id': self.product.id})
        request = self.factory.post(url, form_data)

        # Создаем экземпляр представления
        view = PurchaseCreate.as_view()
        view(request, product_id=self.product.id)

        # Проверяем, что скидка рассчитана правильно
        purchase = Purchase.objects.get(product=self.product, customer=self.customer)
        self.assertEqual(purchase.discount, 15)

    def test_invalid_product(self):
        """Тест попытки создания покупки с неверным продуктом."""
        url = reverse('buy', kwargs={'product_id': 999})  # Неверный ID продукта
        response = self.client.get(url)
        self.assertEqual(response.status_code, 404)

    def test_redirect_after_form_submission(self):
        """Тест перенаправления после успешного создания покупки."""
        form_data = {"address": "Ленина 10", "customer_name": "Иван Иванов"}
        response = self.client.post(reverse('buy', kwargs={'product_id': self.product.id}), form_data)

        # Проверяем успешное перенаправление на чек
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Чек")
        self.assertContains(response, "Иван Иванов")


class ReceiptButtonTestCase(TestCase):
    def setUp(self):
        """Создаем тестовые данные для кнопки возврата."""
        self.customer = Customer.objects.create(name="Иван Иванов", email="ivanov@example.com", total_purchases=3)
        self.product = Product.objects.create(name="Продукт 1", price=100)
        self.purchase = Purchase.objects.create(
            product=self.product,
            customer=self.customer,
            address="Ленина 10",
            discount=5
        )

    def test_back_button_in_receipt(self):
        """Тест кнопки возврата на главную страницу."""
        response = self.client.get(reverse('index'))
        self.assertContains(response, reverse('index'))
