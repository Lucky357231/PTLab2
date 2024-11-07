from django.shortcuts import render, get_object_or_404
from django.views.generic.edit import CreateView
from .models import Product, Purchase, Customer


def index(request):
    products = Product.objects.all()
    message = "Просмотрите наши товары и накопительную систему скидок!"
    context = {
        'products': products,
        'message': message,
    }
    return render(request, 'shop/index.html', context)


class PurchaseCreate(CreateView):
    model = Purchase
    fields = ['address']
    template_name = 'shop/purchase_form.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        product_id = self.kwargs['product_id']
        product = get_object_or_404(Product, id=product_id)
        context['product'] = product
        return context

    def form_valid(self, form):
        customer_name = self.request.POST.get('customer_name')
        customer, created = Customer.objects.get_or_create(name=customer_name)

        # Получаем продукт для покупки
        product_id = self.kwargs['product_id']
        product = get_object_or_404(Product, id=product_id)
        form.instance.product = product
        form.instance.customer = customer

        # Обновляем счетчик покупок
        customer.total_purchases += 1
        customer.save()

        # Рассчитываем скидку и итоговую цену
        discount = 15 if customer.total_purchases > 10 else 0
        discounted_price = int(product.price * (1 - discount / 100))


        # Сохраняем покупку и получаем дату покупки
        purchase = form.save(commit=False)
        purchase.apply_discount()
        purchase.save()

        # Передаем данные в шаблон чека
        context = {
            'customer': customer,
            'product': product,
            'total_purchases': customer.total_purchases,
            'discount': discount,
            'original_price': product.price,
            'discounted_price': discounted_price,
            'purchase_date': purchase.date,
        }
        return render(self.request, 'shop/receipt.html', context)
