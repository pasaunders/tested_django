"""Manage information between login/register pages and the ORM."""


from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, login, logout
from django.views import View
from .forms import signin_form, register_form
from .models import Profile


class SignIn(View):

    def post(self, request, *args, **kwargs):
        if request.POST.get('signin'):
            login = signin_form(request.POST)
            user = authenticate(request, username=login.cleaned_data['username'], password=login.cleaned_data['password'])
            if user is not None:
                login(request, user)
                return redirect(reverse('travel:list'))
            return HttpResponse('invalid password')
        else:
            register = register_form(request.POST)
            if register.is_valid():
                user = User.objects.create_user(
                    username=register.cleaned_data['username'],
                    password=register.cleaned_data['password'],
                    first_name=register.cleaned_data['first_name'],
                    )
                if len(User.objects.all()) is 1:
                    permission = Permission.objects.get(codename='admin')
                else:
                    permission = Permission.objects.get(codename='user')
                user.user_permissions.add(permission)
                login(request, user)
            else:
                context = {
                    'register_form': register_form(),
                    'signin_form': signin_form(),
                    'errors': register.errors.values()

                }
                return render(request, 'login_manager/signin.html', context)
        return redirect(reverse('travel:list'))


    def get(self, request):
        context = {
            'register_form': register_form(),
            'signin_form': signin_form(),
        }
        return render(request, 'login_manager/signin.html', context)


class logout_view(View):

    def get(self, request):
        logout(request)
        return redirect(reverse('login:signin'))
