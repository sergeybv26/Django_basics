import random

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.views.decorators.cache import cache_page
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from mainapp.models import Product, ProductCategory
from basketapp.models import Basket


def get_links_menu():
    if settings.LOW_CACHE:
        key = 'links_menu'
        links_menu = cache.get(key)
        if links_menu is None:
            links_menu = ProductCategory.objects.filter(is_active=True)
            cache.set(key, links_menu)
        return links_menu
    else:
        return ProductCategory.objects.filter(is_active=True)


def get_category(pk):
    if settings.LOW_CACHE:
        key = f'category_{pk}'
        category = cache.get(key)
        if category is None:
            category = get_object_or_404(ProductCategory, pk=pk)
            cache.set(key, category)
        return category
    else:
        return get_object_or_404(ProductCategory, pk=pk)


def get_products():
    if settings.LOW_CACHE:
        key = 'products'
        _products = cache.get(key)
        if _products is None:
            _products = Product.objects.filter(is_active=True, category__is_active=True).select_related('category')
            cache.set(key, _products)
        return _products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).select_related('category')


def get_product(pk):
    if settings.LOW_CACHE:
        key = f'product_{pk}'
        _product = cache.get(key)
        if _product is None:
            _product = get_object_or_404(Product, pk=pk)
            cache.set(key, _product)
        return _product
    else:
        return get_object_or_404(Product, pk=pk)


def get_products_ordered_by_price():
    if settings.LOW_CACHE:
        key = 'products_ordered_by_price'
        _products = cache.get(key)
        if _products is None:
            _products = Product.objects.filter(is_active=True, category__is_active=True).\
                select_related().order_by('price')
            cache.set(key, _products)
        return _products
    else:
        return Product.objects.filter(is_active=True, category__is_active=True).\
                select_related().order_by('price')


def get_products_in_category_ordered_by_price(pk):
    if settings.LOW_CACHE:
        key = f'products_in_category_ordered_by_price_{pk}'
        _products = cache.get(key)
        if _products is None:
            _products = Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).\
                select_related().order_by('price')
            cache.set(key, _products)
        return _products
    else:
        return Product.objects.filter(category__pk=pk, is_active=True, category__is_active=True).\
                select_related().order_by('price')


def get_hot_product():
    return random.sample(list(get_products()), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk).\
                        select_related()[:3]
    return same_products


def main(request):
    context = {
        'title': 'Главная',
        'products': get_products()[:4],
    }
    return render(request, 'mainapp/index.html', context=context)


class ProductsListView(ListView):
    template_name = 'mainapp/products_list.html'
    model = Product
    paginate_by = 2

    def get_queryset(self):
        queryset = super().get_queryset()
        category_pk = self.kwargs.get('pk')

        if category_pk != 0:
            queryset = queryset.filter(category__pk=category_pk)

        return queryset

    def get_context_data(self, *args, **kwargs):
        context_data = super().get_context_data(*args, **kwargs)
        category_pk = self.kwargs.get('pk')

        if category_pk == 0:
            context_data['category'] = {
                'name': 'все',
                'pk': 0
            }
        else:
            context_data['category'] = get_category(category_pk)

        context_data['links_menu'] = get_links_menu()
        context_data['title'] = 'Продукты'

        return context_data


def products_ajax(request, pk=None, page=1):
    if request.is_ajax():
        links_menu = get_links_menu()
        if pk is not None:
            if pk == 0:
                products_list = get_products_ordered_by_price()
                category = {
                    'name': 'все',
                    'pk': 0
                }
            else:
                category = get_category(pk)
                products_list = get_products_in_category_ordered_by_price(pk)

            paginator = Paginator(products_list, 2)
            try:
                products_paginator = paginator.page(page)
            except PageNotAnInteger:
                products_paginator = paginator.page(1)
            except EmptyPage:
                products_paginator = paginator.page(paginator.num_pages)
            context = {
                'products': products_paginator,
                'category': category,
                'links_menu': links_menu,
            }

            result = render_to_string('mainapp/includes/inc_products_list_content.html',
                                      context=context,
                                      request=request)

            return JsonResponse({'result': result})


def products(request):
    title = 'Продукты'
    links_menu = get_links_menu()
    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    context = {
        'links_menu': links_menu,
        'title': title,
        'hot_product': hot_product,
        'same_products': same_products,
    }

    return render(request, 'mainapp/products.html', context=context)


def contact(request):
    context = {
        'title': 'Контакты',
    }
    return render(request, 'mainapp/contact.html', context=context)


def product(request, pk):
    title = 'продукты'

    context = {
        'title': title,
        'links_menu': get_links_menu(),
        'product': get_product(pk),
    }

    return render(request, 'mainapp/product.html', context)
