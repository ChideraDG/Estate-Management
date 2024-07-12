from django.shortcuts import render, redirect
from .forms import *
from .models import *
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User


def register(request):
    form = RegistrationForm()

    if request.method == 'POST':
        form = RegistrationForm(request.POST)

        if form.is_valid():
            cleaned = form.save(commit=False)
            cleaned.password = form.clean_password2()

            user = User.objects.create_user(username=request.POST['email'],
                                            email=request.POST['email'],
                                            password=cleaned.password)
            cleaned.owner_id = user.id

            cleaned.save()

            return redirect('welcome')

    context = {'form': form}
    return render(request, 'estate/register.html', context)


def welcome(request):
    return render(request, 'estate/welcome.html')


def userLogin(request):
    form = LoginForm()

    if request.method == 'POST':
        email = request.POST['user_name']
        password = request.POST['password']

        try:
            user = Registration.objects.get(email=email)
        except:
            print("Email doesn't exist.")

        user = authenticate(request, username=email, password=password)

        if user is not None:
            login(request, user)
            return redirect('welcome')
        else:
            print('Username or Password is Wrong')

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
