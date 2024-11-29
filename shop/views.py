from django.shortcuts import render, get_object_or_404
from django.urls import reverse
from django.views.generic.edit import CreateView
from .models import Product, Purchase, Customer

def index(request):
    products = Product.objects.all()
    context = {
        'products': products,
        'message': "Просмотрите наши товары и накопительную систему скидок!",
    }
    return render(request, 'shop/index.html', context)

class PurchaseCreate(CreateView):
    model = Purchase
    fields = ['address']
    template_name = 'shop/purchase_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['product'] = self._get_product()
        return context

    def form_valid(self, form):
        customer = self._get_or_create_customer()
        product = self._get_product()

        # Обновляем покупки клиента
        customer.total_purchases += 1
        customer.save()

        # Рассчитываем скидку
        discount = self._calculate_discount(customer.total_purchases)
        discounted_price = self._calculate_discounted_price(product.price, discount)

        # Создаем покупку
        purchase = form.save(commit=False)
        purchase.product = product
        purchase.customer = customer
        purchase.discount = discount
        purchase.save()

        # Формируем данные для чека
        context = self._build_receipt_context(
            customer, product, discount, discounted_price, purchase.date
        )
        # Возвращаем страницу чека
        return render(self.request, 'shop/receipt.html', context)

    def _get_product(self):
        """Получает продукт по переданному идентификатору."""
        product_id = self.kwargs['product_id']
        return get_object_or_404(Product, id=product_id)

    def _get_or_create_customer(self):
        """Создает или получает клиента по имени."""
        customer_name = self.request.POST.get('customer_name')
        customer, _ = Customer.objects.get_or_create(name=customer_name)
        return customer

    def _calculate_discount(self, total_purchases):
        """Определяет размер скидки на основе количества покупок."""
        if total_purchases > 10:
            return 15
        elif total_purchases >= 5:
            return 10
        return 5

    def _calculate_discounted_price(self, price, discount):
        """Возвращает цену после применения скидки."""
        return int(price * (1 - discount / 100))

    def _build_receipt_context(self, customer, product, discount, discounted_price, purchase_date):
        """Создает контекст для страницы чека."""
        return {
            'customer': customer,
            'product': product,
            'total_purchases': customer.total_purchases,
            'discount': discount,
            'original_price': product.price,
            'discounted_price': discounted_price,
            'purchase_date': purchase_date,
        }