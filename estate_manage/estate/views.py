from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.contrib import messages


def register(request):
    form = RegistrationForm()
    # form2 = CustomUserCreationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            cleaned = form.save(commit=False)
            cleaned.password = form.clean_password2()
            cleaned.save()

            return redirect('welcome')

    context = {'form': form}
    return render(request, 'estate/register.html', context)


def welcome(request):

    return render(request, 'estate/welcome.html')


def login(request):
    form = LoginForm()

    context = {'form': form}
    return render(request, 'estate/login.html', context)


# def registerUser(request):
#     page = 'register'
#     form = CustomUserCreationForm()
#
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         print(form)
#         print(request.POST)
#
#         # if form.is_valid():
#         #     user = form.save(commit=False)
#         #     user.username = user.username.lower()
#         #     user.save()
#         #
#         #     # messages.success(request, f'{user.username.title()}, your account was created.')
#         #
#         #     # login(request, user)
#         #     return redirect('login')
#
#     context = {'page': page, 'form': form}
#     return render(request, 'estate/test.html', context)
