from django.contrib.auth.decorators import login_required
from django.contrib import auth
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .forms import UserLoginForm, UserUpdateForm, UserRegistrationForm

# Create your views here.

def login(request):
    if request.method == 'POST':
        form = UserLoginForm(data=request.POST)
        if form.is_valid():
            username = request.POST["username"]
            password = request.POST["password"]
            user = auth.authenticate(username=username, password=password)
            if user:
                auth.login(request, user)
                if request.POST.get("next"):
                    return HttpResponseRedirect(request.POST.get("next"))

                return HttpResponseRedirect(reverse('main:index'))

    form = UserLoginForm()

    context = {
        "title": "Авторизация",
        "form": form,
    }

    return render(request, "user/login.html", context)


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(data=request.POST)
        if form.is_valid():
            form.save()
            user = form.instance
            auth.login(request, user)
            return HttpResponseRedirect(reverse('main:index'))

    form = UserRegistrationForm()

    context = {
        "title": "Регистрация",
        "form": form,
    }

    return render(request, "user/register.html", context)

@login_required
def profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(instance=request.user, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('user:profile'))


    form = UserUpdateForm(instance=request.user)

    context = {
        "title": "Профиль",
        "form": form,
    }

    return render(request, "user/profile.html", context)


@login_required
def logout(request):
    auth.logout(request)
    return HttpResponseRedirect(reverse('user:login'))
