from django.urls import path
import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('register/', authapp.register, name='register'),
    path('edit/', authapp.edit, name='edit'),
    path('verify/<email>/<key>/', authapp.verify, name='verify'),
    path('favourite/', authapp.FavouriteListView.as_view(), name='favourite'),
    path('favourite/delete/<int:pk>/', authapp.FavouriteDeleteView.as_view(), name='favourite_delete'),
]
