from django.urls import path

from ordersapp import views as ordersapp

app_name = 'ordersapp'

urlpatterns = [
    path('', ordersapp.OrderListView.as_view(), name='list'),
    path('read/<int:pk>/', ordersapp.OrderDetailView.as_view(), name='read'),
    path('update/<int:pk>/', ordersapp.OrderUpdateView.as_view(), name='update'),
    path('create/', ordersapp.OrderCreateView.as_view(), name='create'),
    path('delete/<int:pk>/', ordersapp.OrderDeleteView.as_view(), name='delete'),
    path('forming/complete/<int:pk>/', ordersapp.order_forming_complete, name='order_forming_complete'),
    path('update/<int:pk_ord>/product/added/<int:pk>/', ordersapp.order_added_product, name='')
]
