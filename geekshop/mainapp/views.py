import random

from django.shortcuts import render, get_object_or_404
from mainapp.models import Product, ProductCategory
from basketapp.models import Basket


def get_basket(user):
    if user.is_authenticated:
        return Basket.objects.filter(user=user)
    else:
        return []


def main(request):
    context = {
        'title': 'Главная',
        'products': Product.objects.all()[:4],
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/index.html', context=context)


def products(request, pk=None):
    title = 'Продукты'
    links_menu = ProductCategory.objects.all()

    if pk is not None:
        if pk == 0:
            products_list = Product.objects.all().order_by('price')
            category = {
                'name': 'все',
                'pk': 0
            }
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category__pk=pk).order_by('price')
        context = {
            'products': products_list,
            'category': category,
            'links_menu': links_menu,
            'title': title,
            'basket': get_basket(request.user)
        }

        return render(request, 'mainapp/products_list.html', context=context)

    hot_product = random.sample(list(Product.objects.all()), 1)[0]
    same_products = Product.objects.all()[3:5]

    context = {
        'links_menu': links_menu,
        'title': title,
        'hot_product': hot_product,
        'same_products': same_products,
        'basket': get_basket(request.user)
    }

    return render(request, 'mainapp/products.html', context=context)


def contact(request):
    context = {
        'title': 'Контакты',
        'basket': get_basket(request.user)
    }
    return render(request, 'mainapp/contact.html', context=context)
