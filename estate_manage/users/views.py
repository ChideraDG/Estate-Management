from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .forms import RegistrationForm, LoginForm, ContactForm, ContactAgentForm, CustomSetPasswordForm, CustomPasswordResetForm
from .models import Profile


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
            return redirect('dashboard')

    context = {'form': form}
    return render(request, 'users/register.html', context)


def home(request):
    return render(request, 'users/home.html')


def userLogin(request):
    form = LoginForm()

    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)

        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']

            user = Profile.objects.filter(username=username_or_email)
            if not user.exists():
                user = Profile.objects.filter(email=username_or_email)
                if not user.exists():
                    print('Account not Found')
                    messages.info(request, 'Account not Found')
                    return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            user = authenticate(request, username=user[0].username, password=password)

            if user is not None:
                login(request, user)
                messages.success(request, f'{user.username.title()}, you successfully logged in.')
                return redirect('dashboard')
            else:
                messages.error(request, 'username or password is wrong')

    context = {'form': form}

    return render(request, 'users/login.html', context)


@login_required(login_url='login')
def userDelete(request):
    user = request.user.profile
    user.delete()
    return redirect('home')


def userLogout(request):
    logout(request)
    return redirect('home')


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm


@login_required(login_url='login')
def dashboard(request):

    user = request.user.profile

    context = {'user': user}
    return render(request, 'dashboard/base.html', context)


def property_single(request):
    form = ContactAgentForm()

    if request.method == 'POST':
        form = ContactAgentForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            subject = 'Estate Manage Agent'
            message = form.cleaned_data.get('message')

            send_mail(from_email=settings.EMAIL_HOST_USER,
                      recipient_list=['chrischidera6@gmail.com'],
                      subject=subject,
                      message=f"Sender's Name: {name.title()} \n\nSender's Email: {email.lower()} \n\n" + message,
                      fail_silently=False)

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid form submission.'})

    context = {'form': form}

    return render(request, 'users/property-single.html', context)


def property_grid(request):
    return render(request, 'users/property-grid.html')


def blog_single(request):
    return render(request, 'users/blog-single.html')


def agents_grid(request):
    return render(request, 'users/agents-grid.html')


def agent_single(request):
    return render(request, 'users/agent-single.html')


def about(request):
    return render(request, 'users/about.html')


def blog(request):
    return render(request, 'users/blog.html')


def contact_us(request):
    form = ContactForm()

    if request.method == 'POST':
        form = ContactForm(request.POST)
        if form.is_valid():
            name = form.cleaned_data.get('name')
            email = form.cleaned_data.get('email')
            subject = form.cleaned_data.get('subject')
            message = form.cleaned_data.get('message')

            send_mail(from_email=settings.EMAIL_HOST_USER,
                      recipient_list=['chrischidera6@gmail.com'],
                      subject=subject,
                      message=f"Sender's Name: {name.title()} \n\nSender's Email: {email.lower()} \n\n" + message,
                      fail_silently=False)

            return JsonResponse({'success': True})
        else:
            return JsonResponse({'success': False, 'error': 'Invalid form submission.'})

    context = {'form': form}

    return render(request, 'users/contact-us.html', context)
