from django.urls import path
from django.views.decorators.cache import cache_page

from mainapp import views as mainapp

app_name = 'mainapp'

urlpatterns = [
    path('', mainapp.products, name='products'),
    path('category/<int:pk>/', mainapp.ProductsListView.as_view(), name='category'),
    # path('category/<int:pk>/ajax/', mainapp.products_ajax),
    # path('category/<int:pk>/page/<int:page>/ajax/', mainapp.products_ajax),
    # path('category/<int:pk>/page/<int:page>/', mainapp.products, name='page'),
    path('product/<int:pk>/', mainapp.product, name='product'),
    path('product/ajax/<int:pk>/', mainapp.add_to_favourite, name='favourite_add'),
]
