from django.shortcuts import render, redirect

# Create your views here.
from Accounts.models import Customer
from .models import Product, Order, OrderProduct
import json
from django.http import JsonResponse

from .forms import AddressForm
from datetime import datetime
from django.views.generic import View, ListView, DetailView, CreateView, UpdateView, DeleteView


class IndexView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer, created = Customer.objects.get_or_create(user=request.user, name=request.user.username, email=request.user.email)
            order, created = Order.objects.get_or_create(customer=customer, completed=False)
        else:
            order = []
        products = Product.objects.order_by('name')
        context = {'order': order}
        return render(request, 'Ecommerce/index.html', context)


class StoreView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer, created = Customer.objects.get_or_create(user=request.user, name=request.user.username, email=request.user.email)
            order, created = Order.objects.get_or_create(customer=customer, completed=False)
            orderproducts = order.orderproduct_set.all().order_by('product__name')
        else:
            order = {'cart_total_items': 0, 'cart_total_price': 0}
            orderproducts = []

        products = Product.objects.order_by('name')
        context = {'products': products, 'order': order, 'orderproducts': orderproducts}
        return render(request, 'Ecommerce/store.html', context)


class UpdateItemView(View):
    """Backend umożliwiający zalogowanemu użytkownikowi dodawanie/usuwanie produktów z koszyka."""
    def post(self, request, *args, **kwargs):
        data = json.loads(request.body)
        productId = data['productId']                                                                                   # values from cart.js
        action = data['action']

        product = Product.objects.get(id=productId)
        order = Order.objects.get(customer=request.user.customer, completed=False)
        orderProduct, created = OrderProduct.objects.get_or_create(product=product, order=order)

        if action == 'add':
            orderProduct.quantity += 1
        elif action == 'remove':
            orderProduct.quantity -= 1

        orderProduct.save()

        if orderProduct.quantity <= 0:
            orderProduct.delete()

        return JsonResponse('Cart has been updated.', safe=False)


class CheckoutView(View):
    def get(self, request, *args, **kwargs):
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, completed=False)
            orderproducts = order.orderproduct_set.all().order_by('product__name')
            form = AddressForm()
        else:
            order = {'cart_total_price': 0, 'cart_total_items': 0}
            orderproducts = []
            form = []

        context = {'order': order, 'orderproducts': orderproducts, 'form': form}
        return render(request, 'Ecommerce/checkout.html', context)

    def post(self, request, *args, **kwargs):
        form = AddressForm(request.POST)
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        if form.is_valid():
            new_form = form.save(commit=False)
            new_form.customer = customer
            new_form.order = order
            new_form.save()
            form.save
            return redirect('process_order')


class ProcessOrderView(View):
    def get(self, request, *args, **kwargs):
        transaction_id = datetime.now().timestamp()                                                                     # transaction_id = datetime.now().strftime('%Y%m-%d%H-%M%S-') + str(uuid.uuid4()) # 202006-1914-5710-ee3700db-a27a-4cf7-ba8f-ae17fbfda2e7

        if request.user.is_authenticated:
            customer = request.user.customer
            Order.objects.filter(customer=customer, completed=False).update(completed=True, transaction_id=transaction_id)

            return render(request, 'Ecommerce/process_order.html')
