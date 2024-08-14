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
from .forms import (RegistrationForm, LoginForm, ContactForm, ContactAgentForm, 
                    CustomSetPasswordForm, CustomPasswordResetForm, ProfileForm)
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
                
                designation = request.user.profile.designation
                if designation == "building_owner":
                    return redirect('view-building-owner', request.user.profile.id)
                elif designation == "agent":
                    return redirect('dashboard-A', request.user.profile.username)
                elif designation == "buyer":
                    return redirect('dashboard-B', request.user.profile.username)
                elif designation == "company":
                    return redirect('dashboard-C', request.user.profile.username)
                elif designation == "tenant":
                    return redirect('dashboard-T', request.user.profile.username)
            else:
                messages.error(request, 'username or password is wrong')
        else:
            print("Form not valid")
    else:
        form = LoginForm()

    context = {'form': form}

    return render(request, 'users/login.html', context)


@login_required(login_url='login')
def userView(request, pk):
    profile = Profile.objects.get(username=pk)

    context = {"user": profile}
    return render(request, "users/view-user.html", context)


@login_required(login_url='login')
def userUpdate(request, pk):
    profile = Profile.objects.get(username=pk)
    form = ProfileForm(instance=profile)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            instance = form.save(commit=False)
            instance.name = instance.name.strip().title()
            instance.email = instance.email.strip().lower()

            instance.save()
            messages.success(request, 'Profile updated successfully')
            return redirect('view-user-profile', pk=instance.username)

    return render(request, 'users/update-profile.html', {'form': form})

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
    designation = request.user.profile.designation
    if designation == "building_owner":
        return redirect('dashboard-BO', request.user.profile.username)
    elif designation == "agent":
        return redirect('dashboard-A', request.user.profile.username)
    elif designation == "buyer":
        return redirect('dashboard-B', request.user.profile.username)
    elif designation == "company":
        return redirect('dashboard-C', request.user.profile.username)
    elif designation == "tenant":
        return redirect('dashboard-T', request.user.profile.username)


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
