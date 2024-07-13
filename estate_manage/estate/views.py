from django.contrib import messages
from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User


def userRegister(request):
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            cleaned = form.save(commit=False)
            cleaned.password = form.clean_password2()
            cleaned.full_name = cleaned.full_name.title().strip()

            user = User.objects.create_user(username=request.POST['email'],
                                            email=request.POST['email'],
                                            password=cleaned.password)
            cleaned.owner_id = user.id

            cleaned.save()

            login(request, user)
            return redirect('welcome')

    context = {'form': form}
    return render(request, 'estate/register.html', context)


def welcome(request):
    return render(request, 'estate/welcome.html')


def userLogin(request):
    form = LoginForm()

    if request.user.is_authenticated:
        return redirect('welcome')

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            email = form.cleaned_data['email']
            password = form.cleaned_data['password']

            try:
                user = Registration.objects.get(email=email)
            except:
                print("Email doesn't exist.")

            user = authenticate(request, username=email, password=password)
            print(user)

            if user is not None:
                login(request, user)
                return redirect('welcome')
            else:
                messages.error(request, 'username or password is wrong')

    context = {'form': form}

    return render(request, 'estate/login.html', context)


def userLogout(request):
    logout(request)
    return redirect('welcome')
