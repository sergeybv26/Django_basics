from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.generic import ListView

from authapp.forms import ShopUserLoginForm, ShopUserRegisterForm, ShopUserEditForm, ShopUserProfileEditForm
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.urls import reverse

from authapp.models import ShopUser, ShopUserFavourite
from authapp.services import send_verify_mail


class AccessMixin:
    @method_decorator(login_required())
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


def login(request):
    title = 'вход'

    login_form = ShopUserLoginForm(data=request.POST or None)

    next_param = request.GET.get('next', '')

    if request.method == 'POST' and login_form.is_valid():
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(username=username, password=password)
        if user and user.is_active:
            auth.login(request, user)
            if 'next' in request.POST.keys():
                return HttpResponseRedirect(request.POST['next'])
            else:
                return HttpResponseRedirect(reverse('index'))

    context = {
        'title': title,
        'login_form': login_form,
        'next': next_param
    }
    return render(request, 'authapp/login.html', context)


def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('index'))


def register(request):
    title = 'регистрация'

    if request.method == 'POST':
        register_form = ShopUserRegisterForm(request.POST, request.FILES)

        if register_form.is_valid():
            new_user = register_form.save()
            send_verify_mail(new_user)
            return HttpResponseRedirect(reverse('auth:login'))
    else:
        register_form = ShopUserRegisterForm()

    context = {
        'title': title,
        'register_form': register_form
    }

    return render(request, 'authapp/register.html', context)


@transaction.atomic
def edit(request):
    title = 'Редактирование'

    if request.method == 'POST':
        edit_form = ShopUserEditForm(request.POST, request.FILES, instance=request.user)
        profile_form = ShopUserProfileEditForm(request.POST, instance=request.user.shopuserprofile)
        if edit_form.is_valid() and profile_form.is_valid():
            edit_form.save()
            return HttpResponseRedirect(reverse('auth:edit'))
    else:
        edit_form = ShopUserEditForm(instance=request.user)
        profile_form = ShopUserProfileEditForm(instance=request.user.shopuserprofile)
    context = {
        'title': title,
        'edit_form': edit_form,
        'profile_form': profile_form,
    }

    return render(request, 'authapp/edit.html', context)


def verify(request, email, key):
    user = ShopUser.objects.filter(email=email).first()
    if user:
        if user.activation_key == key and not user.is_activation_key_expired():
            user.activate_user()
            auth.login(request, user, backend='django.contrib.auth.backends.ModelBackend')

    return render(request, 'authapp/register_result.html')


class FavouriteListView(AccessMixin, ListView):
    model = ShopUserFavourite
    template_name = 'authapp/favourite.html'

    def get_queryset(self):
        return ShopUserFavourite.objects.all().select_related()


