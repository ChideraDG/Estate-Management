from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth import get_user_model


def userRegister(request):
    form = RegistrationForm()

    if request.user.is_authenticated:
        return redirect('welcome')

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
            return redirect('welcome')

    context = {'form': form}
    return render(request, 'users/register.html', context)


def welcome(request):
    return render(request, 'users/welcome.html')


def userLogin(request):
    form = LoginForm()

    if request.user.is_authenticated:
        return redirect('welcome')

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username = form.cleaned_data['username']
            password = form.cleaned_data['password']

            try:
                user = Profile.objects.get(username=username)
            except:
                print("Username doesn't exist.")

            user = authenticate(request, username=username, password=password)

            if user is not None:
                login(request, user)
                return redirect('welcome')
            else:
                messages.error(request, 'username or password is wrong')

    context = {'form': form}

    return render(request, 'users/login.html', context)


def userLogout(request):
    logout(request)
    return redirect('welcome')


def test(request):
    return render(request, 'users/welcome.html')
