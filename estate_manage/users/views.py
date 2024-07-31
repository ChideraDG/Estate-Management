from django.contrib import messages
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model
from django.contrib import messages


def userRegister(request):
    form = RegistrationForm()

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            user = User.objects.create_user(username=request.POST['username'],
                                            email=request.POST['email'].lower(),
                                            password=form.clean_password2(),
                                            first_name=request.POST['full_name'].title(),
                                            last_name=request.POST['designation'])

            user.last_name = ''
            user.save()

            login(request, user)
            return redirect('home')

    context = {'form': form}
    return render(request, 'users/register.html', context)


def home(request):
    return render(request, 'users/home.html')


def userLogin(request):
    form = LoginForm()

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            user = Profile.objects.filter(username=username)
            if not user.exists():
                print('Account not Found')
                messages.info(request, 'Account not Found')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'{user.username.title()}, you successfully logged in.')
                return redirect('home')
            else:
                messages.error(request, 'username or password is wrong')

    context = {'form': form}

    return render(request, 'users/login.html', context)


def userLogout(request):
    logout(request)
    return redirect('home')
