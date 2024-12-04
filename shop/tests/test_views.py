from django.test import TestCase, RequestFactory
from django.urls import reverse
from django.http import Http404
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
        view.object = None

        context = view.get_context_data()
        self.assertIn('product', context)
        self.assertEqual(context['product'], self.product)

    def test_form_valid_creates_purchase(self):
        """Тест создания покупки через form_valid."""
        form_data = {"address": "Ленина 10", "customer_name": "Иван Иванов"}
        url = reverse('buy', kwargs={'product_id': self.product.id})
        request = self.factory.post(url, form_data)

        view = PurchaseCreate.as_view()
        response = view(request, product_id=self.product.id)
        self.assertEqual(response.status_code, 200)

        purchase = Purchase.objects.get(product=self.product, customer=self.customer)
        self.assertEqual(purchase.address, "Ленина 10")
        self.assertEqual(purchase.discount, 10)

    def test_redirect_after_form_submission(self):
        """Тест перенаправления после успешного создания покупки."""
        form_data = {"address": "Ленина 10", "customer_name": "Иван Иванов"}
        response = self.client.post(reverse('buy', kwargs={'product_id': self.product.id}), form_data)
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Чек")
        self.assertContains(response, "Иван Иванов")


class PurchaseCreateHelperMethodsTestCase(TestCase):
    def setUp(self):
        self.factory = RequestFactory()
        self.product = Product.objects.create(name="Продукт 1", price=100)
        self.customer = Customer.objects.create(name="Иван Иванов", total_purchases=5)
        self.view = PurchaseCreate()

    def test_get_product_valid_id(self):
        """Тест получения продукта по валидному ID."""
        self.view.kwargs = {'product_id': self.product.id}
        result = self.view._get_product()
        self.assertEqual(result, self.product)

    def test_get_product_invalid_id(self):
        """Тест обработки неверного ID продукта."""
        self.view.kwargs = {'product_id': 999}
        with self.assertRaises(Http404):
            self.view._get_product()


    def test_calculate_discount(self):
        """Тест расчета скидки."""
        self.assertEqual(self.view._calculate_discount(4), 5)
        self.assertEqual(self.view._calculate_discount(5), 10)
        self.assertEqual(self.view._calculate_discount(12), 15)

    def test_calculate_discounted_price(self):
        """Тест расчета цены со скидкой."""
        self.assertEqual(self.view._calculate_discounted_price(100, 10), 90)
        self.assertEqual(self.view._calculate_discounted_price(200, 0), 200)
        self.assertEqual(self.view._calculate_discounted_price(150, 15), 127)

    def test_build_receipt_context(self):
        """Тест формирования контекста чека."""
        context = self.view._build_receipt_context(
            customer=self.customer,
            product=self.product,
            discount=10,
            discounted_price=90,
            purchase_date="2024-11-23"
        )
        self.assertEqual(context['customer'], self.customer)
        self.assertEqual(context['product'], self.product)
        self.assertEqual(context['total_purchases'], 5)
        self.assertEqual(context['discount'], 10)
        self.assertEqual(context['original_price'], 100)
        self.assertEqual(context['discounted_price'], 90)
        self.assertEqual(context['purchase_date'], "2024-11-23")
