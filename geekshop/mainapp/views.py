from django.shortcuts import render
from mainapp.models import Product, ProductCategory


def main(request):
    context = {
        'title': 'Главная',
        'products': Product.objects.all()[:4]
    }
    return render(request, 'mainapp/index.html', context=context)


product_list = [
    {
        'title': 'отличный стул',
        'price': '2585.9'
    }
]


def products(request, pk=None):
    context = {
        'products': product_list,
        'links_menu': ProductCategory.objects.all(),
        'title': 'Продукты'
    }

    return render(request, 'mainapp/products.html', context=context)


def contact(request):
    context = {
        'title': 'Контакты'
    }
    return render(request, 'mainapp/contact.html', context=context)
