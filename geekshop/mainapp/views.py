import json
import os
import random
from datetime import date
from urllib import request
from xml.dom import minidom

from django.conf import settings
from django.core.cache import cache
from django.http import JsonResponse, Http404, HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.template.loader import render_to_string
from django.urls import reverse
from django.views.decorators.cache import cache_page
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from authapp.models import ShopUserFavourite
from mainapp.models import Product, ProductCategory, ExchangeRate
from basketapp.models import Basket


def get_exchange_rate():
    rate = ExchangeRate.objects.filter(rate_update_at=date.today()).first()

    if not rate:
        url = 'http://www.cbr.ru/scripts/XML_daily.asp'
        web_xml = request.urlopen(url)
        xml_data = web_xml.read()

        filename = os.path.join(settings.BASE_DIR, 'tmp') + '/exchange.xml'
        with open(filename, 'wb') as local_xml:
            local_xml.write(xml_data)
            local_xml.close()

        xml = minidom.parse(filename)
        currency = xml.getElementsByTagName('Valute')
        for element in currency:
            charcode = element.getElementsByTagName('CharCode')[0].firstChild.data
            if charcode == 'USD':
                value = float(element.getElementsByTagName('Value')[0].firstChild.data.replace(',', '.'))
                rate = ExchangeRate(rate=value)
                rate.save()
                break

    return rate


def get_usd():
    if settings.LOW_CACHE:
        key = 'usd_exchange'
        usd_exchange = cache.get(key)
        if usd_exchange is None:
            usd_exchange = get_exchange_rate().rate
            cache.set(key, usd_exchange)
        return usd_exchange
    else:
        return get_exchange_rate().rate


def get_price_usd(product_price):
    return product_price / get_usd()


def get_favourite(user, pk):
    return ShopUserFavourite.objects.filter(user=user, product__pk=pk).first()


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
    try:
        _hot_product = random.sample(list(get_products()), 1)[0]
    except ValueError:
        raise Http404('Отсутствуют продукты в базе данных')
    return _hot_product


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk).\
                        select_related()[:3]
    return same_products


def main(request):

    context = {
        'title': 'Главная',
        'products': get_products()[:4],
        'exchange_rate': get_usd()
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
        context_data['exchange_rate'] = get_usd()

        return context_data


def products_ajax(request, pk=None, page=1):
    print('controller ajax1')
    if request.is_ajax():
        print('controller ajax')
        links_menu = get_links_menu()
        if pk is not None:
            print(f'pk={pk}')
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
            print(products_list)
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
            print(f'paginator: {products_paginator}')
            print(f'object_list: {products_paginator.object_list}')
            result = render_to_string('mainapp/includes/inc_products_list_content.html',
                                      context=context,
                                      request=request)
            print(result)
            return JsonResponse({'result': result})


def products(request, pk=None, page=1):
    title = 'Продукты'
    links_menu = get_links_menu()
    # print('controller products')
    # if pk is not None:
    #     if pk == 0:
    #         products_list = get_products_ordered_by_price()
    #         category = {
    #             'name': 'все',
    #             'pk': 0
    #         }
    #     else:
    #         category = get_object_or_404(ProductCategory, pk=pk)
    #         products_list = get_products_in_category_ordered_by_price(pk)
    #
    #     paginator = Paginator(products_list, 2)
    #     print(products_list)
    #     try:
    #         products_paginator = paginator.page(page)
    #     except PageNotAnInteger:
    #         products_paginator = paginator.page(1)
    #     except EmptyPage:
    #         products_paginator = paginator.page(paginator.num_pages)
    #     context = {
    #         'products': products_paginator,
    #         'category': category,
    #         'links_menu': links_menu,
    #         'title': title,
    #     }
    #
    #     return render(request, 'mainapp/products_list.html', context=context)

    hot_product = get_hot_product()
    same_products = get_same_products(hot_product)

    context = {
        'links_menu': links_menu,
        'title': title,
        'hot_product': hot_product,
        'same_products': same_products,
        'exchange_rate': get_usd(),
        'price_usd': get_price_usd(hot_product.price),
    }

    return render(request, 'mainapp/products.html', context=context)


def contact(request):
    context = {
        'title': 'Контакты',
        'exchange_rate': get_usd(),
    }
    return render(request, 'mainapp/contact.html', context=context)


def product(request, pk):
    title = 'продукты'
    _product = get_product(pk)
    context = {
        'title': title,
        'links_menu': get_links_menu(),
        'product': _product,
        'favourite': get_favourite(request.user, pk),
        'exchange_rate': get_usd(),
        'price_usd': get_price_usd(_product.price)
    }

    return render(request, 'mainapp/product.html', context)


def add_to_favourite(request, pk):
    _favourite_item = get_favourite(request.user, pk)

    if not _favourite_item:
        _favourite_item = ShopUserFavourite(user=request.user, product=get_product(pk))
        _favourite_item.save()

    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


@csrf_exempt
def product_upload(request):
    if request.method == 'POST':
        if request.headers.get('Authorization') == settings.UPLOAD_TOKEN:
            filename = os.path.join(settings.BASE_DIR, 'tmp') + '/product.json'
            data = request.body.decode('utf-8')
            with open(filename, 'w', encoding='utf-8') as local_json:
                local_json.write(data)
                local_json.close()
            with open(filename, 'r', encoding='utf-8') as json_file:
                json_data = json.load(json_file)
                json_file.close()

            for _product in json_data:
                category_name = _product['category']
                _category = ProductCategory.objects.get(name=category_name)
                _product['category'] = _category
                Product.objects.create(**_product)
            return HttpResponse('Данные загружены')
    raise Http404()
