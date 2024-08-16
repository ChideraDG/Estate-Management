from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from .forms import LoginForm
from .models import Profile
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


def user_register(request):
    form = RegistrationForm(request.POST if request.method == 'POST' else None)

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST' and form.is_valid():
        user = User.objects.create_user(
            username=form.cleaned_data['username'],
            email=form.cleaned_data['email'].lower(),
            password=form.cleaned_data['password2'],
            first_name=form.cleaned_data['full_name'].title(),
            last_name=form.cleaned_data['designation']
        )

        user.last_name = ''
        user.save()

        login(request, user)
        messages.success(request, f'{user.username.title()}, Welcome to Estate Manage')

        designation = request.user.profile.designation
        redirects = {
            "building_owner": 'update-user-profile',
            "agent": 'dashboard-A',
            "buyer": 'dashboard-B',
            "company": 'dashboard-C',
            "tenant": 'dashboard-T'
        }
        return redirect(redirects.get(designation, 'home'), request.user.profile)
    elif request.method == 'POST':
        messages.error(request, form.get_error())

    context = {'form': form}
    return render(request, 'users/register.html', context)


def home(request):
    return render(request, 'users/home.html')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            username_or_email = form.cleaned_data['username_or_email']
            password = form.cleaned_data['password']

            user = Profile.objects.filter(username=username_or_email).first() or Profile.objects.filter(email=username_or_email).first()
            if not user:
                messages.info(request, 'Account not Found')
                return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

            user = authenticate(request, username=user.username, password=password)
            if user is not None:
                login(request, user)
                messages.success(request, f'{user.username.title()}, you successfully logged in.')
                
                designation = user.profile.designation
                labels = {"building_owner": "BO", "agent": "A", "buyer": "B", "company": "C", "tenant": "T"}
                return redirect(f'dashboard-{labels.get(designation)}', user.profile)
            else:
                messages.error(request, 'Password is wrong')
        else:
            messages.warning(request, 'Form not Valid')
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'users/login.html', context)


@login_required(login_url='login')
def user_view(request, pk):
    profile = Profile.objects.get(username=pk)

    active_menu = 'user-management'
    active_sub_menu = 'personal-profile'

    context = {
        "user": profile,
        "active_menu": active_menu,
        "active_sub_menu": active_sub_menu
    }

    return render(request, "users/view-user.html", context)


@login_required(login_url='login')
def user_update(request, pk):
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
    
    active_menu = 'user-management'
    active_sub_menu = 'personal-profile'

    context = {
        "user": profile,
        "active_menu": active_menu,
        "active_sub_menu": active_sub_menu,
        'form': form
    }

    return render(request, 'users/update-profile.html', context)

@login_required(login_url='login')
def user_delete(request):
    user = request.user.profile
    user.delete()
    return redirect('home')

@login_required(login_url='login')
def user_logout(request):
    logout(request)
    return redirect('home')


class CustomPasswordResetView(PasswordResetView):
    form_class = CustomPasswordResetForm

    def form_invalid(self, form):
        error_message = form.get_error(self.request.POST['email'])
        messages.error(self.request, error_message)
        return super().form_invalid(form)


class CustomPasswordResetConfirmView(PasswordResetConfirmView):
    form_class = CustomSetPasswordForm

    def form_invalid(self, form):
        print(self.request.POST)
        error_message = form.get_error(self.request.POST['new_password1'], self.request.POST['new_password2'])
        messages.error(self.request, error_message)
        return super().form_invalid(form)


@login_required(login_url='login')
def dashboard(request):
    designation = request.user.profile.designation
    dashboard_mapping = {
        "building_owner": 'dashboard-BO',
        "agent": 'dashboard-A',
        "buyer": 'dashboard-B',
        "company": 'dashboard-C',
        "tenant": 'dashboard-T'
    }
    return redirect(dashboard_mapping.get(designation), request.user.profile)


def property_single(request):
    form = ContactAgentForm(request.POST if request.method == 'POST' else None)

    if request.method == 'POST' and form.is_valid():
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
    elif request.method == 'POST':
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
    form = ContactForm(request.POST if request.method == 'POST' else None)

    if request.method == 'POST' and form.is_valid():
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
    elif request.method == 'POST':
        return JsonResponse({'success': False, 'error': 'Invalid form submission.'})

    context = {'form': form}

    return render(request, 'users/contact-us.html', context)
