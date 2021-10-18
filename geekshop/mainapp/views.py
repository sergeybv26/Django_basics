from django.shortcuts import render

# Create your views here.


def main(request):
    context = {
        'title': 'Главная',
    }
    return render(request, 'mainapp/index.html', context=context)


product_list = [
    {
        'title': 'отличный стул',
        'price': '2585.9'
    }
]

links_menu = [
    {
        'url': 'products',
        'title': 'все'
    },
    {
        'url': 'products_home',
        'title': 'дом'
    },

    {
        'url': 'products_office',
        'title': 'офис'
    },

    {
        'url': 'products_modern',
        'title': 'модерн'
    },

    {
        'url': 'products_classic',
        'title': 'классика'
    }
]


def products(request):
    context = {
        'products': product_list,
        'links_menu': links_menu,
        'title': 'Продукты'
    }

    return render(request, 'mainapp/products.html', context=context)


def products_home(request):
    context = {
        'products': product_list,
        'links_menu': links_menu,
        'title': 'Продукты для дома'
    }

    return render(request, 'mainapp/products.html', context=context)


def products_office(request):
    context = {
        'products': product_list,
        'links_menu': links_menu,
        'title': 'Продукты для офиса'
    }

    return render(request, 'mainapp/products.html', context=context)


def products_modern(request):
    context = {
        'products': product_list,
        'links_menu': links_menu,
        'title': 'Продукты модерн'
    }

    return render(request, 'mainapp/products.html', context=context)


def products_classic(request):
    context = {
        'products': product_list,
        'links_menu': links_menu,
        'title': 'Продукты классика'
    }

    return render(request, 'mainapp/products.html', context=context)


def contact(request):
    context = {
        'title': 'Контакты'
    }
    return render(request, 'mainapp/contact.html', context=context)
