from django.test import TestCase
from django.urls import reverse
from shop.models import Product, Purchase, Customer


class IndexViewTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Тестовый продукт", price=1000)

    def test_index_view(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/index.html')
        self.assertIn('message', response.context)
        self.assertEqual(response.context['message'], "Просмотрите наши товары и накопительную систему скидок!")
        self.assertIn('products', response.context)
        self.assertEqual(list(response.context['products']), [self.product])


class PurchaseCreateViewTests(TestCase):
    def setUp(self):
        self.product = Product.objects.create(name="Тестовый продукт", price=1000)
        self.customer = Customer.objects.create(name="Иван Иванов", total_purchases=5)

    def test_purchase_create_view_get(self):
        response = self.client.get(reverse('buy', kwargs={'product_id': self.product.id}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/purchase_form.html')
        self.assertEqual(response.context['product'], self.product)

    def test_purchase_create_view_post(self):
        data = {
            'customer_name': self.customer.name,
            'address': '123 Test Street'
        }
        response = self.client.post(reverse('buy', kwargs={'product_id': self.product.id}), data=data)

        self.customer.refresh_from_db()
        self.assertEqual(self.customer.total_purchases, 6)

        # Логика расчета скидки
        expected_discount = 15 if self.customer.total_purchases > 10 else 0
        expected_discounted_price = int(self.product.price * (1 - expected_discount / 100))

        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'shop/receipt.html')
        self.assertEqual(response.context['customer'], self.customer)
        self.assertEqual(response.context['product'], self.product)
        self.assertEqual(response.context['total_purchases'], self.customer.total_purchases)
        self.assertEqual(response.context['discount'], expected_discount)
        self.assertEqual(response.context['original_price'], self.product.price)
        self.assertEqual(response.context['discounted_price'], expected_discounted_price)
        self.assertIsNotNone(response.context['purchase_date'])

        # Проверка значения discounted_price
        purchase = Purchase.objects.latest('date')
        self.assertEqual(purchase.product, self.product)
        self.assertEqual(purchase.customer, self.customer)
        self.assertEqual(purchase.address, data['address'])

