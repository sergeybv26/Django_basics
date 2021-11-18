import random

from django.shortcuts import render, get_object_or_404
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import ListView, CreateView, UpdateView, DetailView, DeleteView

from mainapp.models import Product, ProductCategory
from basketapp.models import Basket


def get_hot_product():
    return random.sample(list(Product.objects.all()), 1)[0]


def get_same_products(hot_product):
    same_products = Product.objects.filter(category=hot_product.category).exclude(pk=hot_product.pk)[:3]
    return same_products


def main(request):
    context = {
        'title': 'Главная',
        'products': Product.objects.all()[:4],
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
            context_data['category'] = ProductCategory.objects.get(pk=category_pk)
        context_data['links_menu'] = ProductCategory.objects.filter(is_active=True)
        context_data['title'] = 'Продукты'

        return context_data


def products(request, pk=None, page=1):
    title = 'Продукты'
    links_menu = ProductCategory.objects.filter(is_active=True)

    if pk is not None:
        if pk == 0:
            products_list = Product.objects.filter(is_active=True, category__is_active=True).order_by('price')
            category = {
                'name': 'все',
                'pk': 0
            }
        else:
            category = get_object_or_404(ProductCategory, pk=pk)
            products_list = Product.objects.filter(category__pk=pk,
                                                   is_active=True, category__is_active=True).order_by('price')

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
            'title': title,
        }

        return render(request, 'mainapp/products_list.html', context=context)

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
        'links_menu': ProductCategory.objects.all(),
        'product': get_object_or_404(Product, pk=pk),
    }

    return render(request, 'mainapp/product.html', context)
