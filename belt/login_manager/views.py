"""Manage information between login/register pages and the ORM."""


from django.shortcuts import render, redirect, HttpResponse
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User, Permission
from django.contrib.auth import authenticate, login, logout
from .forms import signin_form, register_form
from .models import Profile
from django.views import View


class index(View):

    def get(self, request):
        return render(request, 'login_manager/index.html')


class signin(View):

    def post(self, request, *args, **kwargs):
        if request.POST.get('signin'):
            user = authenticate(request, username=request.POST['email'], password=request.POST['password'])
            if user is not None:
                login(request, user)
                import pdb; pdb.set_trace()
                return redirect(reverse('login:home'))
            return HttpResponse('invalid password')
        else:
            user = User.objects.create_user(
                username=request.POST['email'],
                email=request.POST['email'],
                password=request.POST['password'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                )
            import pdb; pdb.set_trace()
            if len(User.objects.all()) is 1:
                permission = Permission.objects.get(codename='admin')
            else:
                permission = Permission.objects.get(codename='user')
            user.user_permissions.add(permission)
            import pdb; pdb.set_trace()
            # add normal user permisisons for other models
            login(request, user)
        return redirect(reverse('login:home'))


    def get(self, request):
        context = {
            'register_form': register_form,
            'signin_form': signin_form,
        }
        return render(request, 'login_manager/signin.html', context)


class logout_view(View):

    def get(self, request):
        logout(request)
        return redirect(reverse('login:home'))
