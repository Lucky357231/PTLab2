from django.test import TestCase, Client
from django.urls import reverse
from shop.models import Product, Purchase

class PurchaseCreateTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.product = Product.objects.create(name="book", price=740)

    def test_webpage_accessibility(self):
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 200)

    def test_create_purchase_with_discount(self):
        response = self.client.post(reverse('buy', args=[self.product.id]), {
            'person': 'Ivanov',
            'email': 'ivanov@example.com',
            'address': 'Svetlaya St.'
        })
        self.assertEqual(response.status_code, 200)
        self.assertIn(b'Спасибо за покупку, Ivanov!', response.content)

        # Проверяем, что покупка создалась в базе данных
        purchase = Purchase.objects.get(customer_name='Ivanov')
        self.assertEqual(purchase.product, self.product)
        self.assertEqual(purchase.customer_email, 'ivanov@example.com')
