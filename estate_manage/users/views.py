import random
import string
import socket
from datetime import datetime, timedelta
from django.utils import timezone
from django.utils.text import slugify
from django.shortcuts import render, redirect
from django.urls import reverse, reverse_lazy
from django.contrib import messages
from django.http import HttpResponseRedirect
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.http import HttpResponseRedirect, JsonResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import PasswordResetView
from django.contrib.auth.views import PasswordResetConfirmView
from django.contrib.auth.views import PasswordChangeView
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.models import User
from .forms import LoginForm
from .models import Profile
from .forms import (RegistrationForm, LoginForm, ContactForm, ContactAgentForm, 
                    CustomSetPasswordForm, CustomPasswordResetForm, ProfileForm, 
                    CustomPasswordChangeForm)
from .models import Profile, ActivityLog


def user_register(request):
    form = RegistrationForm(request.POST if request.method == 'POST' else None)

    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST' and form.is_valid():
        if not check_network_connection():
            return JsonResponse({"error": "No network connection. Please check your internet."}, status=500)
    
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
            "building_owner": 'view-building-owner',
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
    next_url = request.GET.get('next', '/')

    context = {
        'next_url': next_url
    }
    return render(request, 'users/home.html', context)


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
                
                next_url = request.GET.get("next", f'dashboard-{labels.get(designation)}')
                return redirect(next_url, user.profile)
            else:
                messages.error(request, 'Password is wrong')
        else:
            messages.warning(request, 'Form not Valid')
    else:
        form = LoginForm()

    context = {'form': form}
    return render(request, 'users/login.html', context)


@login_required(login_url='login')
def user_profile(request, type, pk):
    profile = Profile.objects.get(username=pk)

    if request.method == "POST":
        form = ProfileForm(request.POST, request.FILES, instance=profile, request=request)

        if form.is_valid():
            instance = form.save(commit=False)
            old_instance = Profile.objects.get(username=pk)
            
            instance.name = instance.name.strip().title()
            instance.email = instance.email.strip().lower()
            if not instance.profile_image:
                instance.profile_image = 'person_1.jpg'

            # Track changes
            changes = []
            for field in form.changed_data:
                original_value = getattr(old_instance, field)
                new_value = getattr(instance, field)
                if original_value != new_value:
                    changes.append(field)
                
            instance.save()

            if changes:
                messages.success(request, 'Profile Updated!')
    else:
        form = ProfileForm(instance=profile)

    menu = 'user-management'
    s_menu = 'personal-profile'

    template_routes = {
        'building_owner': "building_owners/BO_dashboard.html",
        'tenant': "tenants/T_dashboard.html",
        'agent': "agents/A_dashboard.html",
        'company': "companies/C_dashboard.html",
        'buyer': "buyers/B_dashboard.html",
    }
    connection_route = {
        'building_owner': "bo-view-connections",
        'tenant': "t-view-connections",
        'agent': "a-view-connections",
        'company': "c-view-connections",
        'buyer': "b-view-connections"
    }

    context = {
        "user": profile,
        "menu": menu,
        "s_menu": s_menu,
        "type": type,
        'form': form,
        'template_routes': template_routes.get(profile.designation),
        'connection_route': connection_route.get(profile.designation)
    }

    return render(request, "users/user-profile.html", context)

class CustomPasswordChangeView(LoginRequiredMixin, PasswordChangeView):
    form_class = CustomPasswordChangeForm
    template_name = 'users/user-change-password.html'
    login_url = reverse_lazy('login')

    def get_success_url(self) -> str:
        return reverse('view-user-profile', kwargs={
            'pk': self.kwargs['pk'],
            'type': self.kwargs['type']
        })
    
    menu = 'user-management'
    s_menu = 'personal-profile'

    template_routes = {
        'building_owner': "building_owners/BO_dashboard.html",
        'tenant': "tenants/T_dashboard.html",
        'agent': "agents/A_dashboard.html",
        'company': "companies/C_dashboard.html",
        'buyer': "buyers/B_dashboard.html",
    }

    connection_route = {
        'building_owner': "bo-view-connections",
        'tenant': "t-view-connections",
        'agent': "a-view-connections",
        'company': "c-view-connections",
        'buyer': "b-view-connections",
    }

    def get_context_data(self, **kwargs):
        # Get the existing context
        context = super().get_context_data(**kwargs)
        
        # Capture the URL parameters 'type' and 'pk'
        context['type'] = self.kwargs['type']
        context['pk'] = self.kwargs['pk']
        context['connection_route'] = self.connection_route.get(self.request.user.profile.designation, None)
        context['menu'] = self.menu
        context['s_menu'] = self.s_menu
        context['template_routes'] = self.template_routes.get(self.request.user.profile.designation, None)
        
        return context

    def form_valid(self, form):
        # Add the success message
        messages.success(self.request, 'Your password has been successfully changed.')
        return super().form_valid(form)
    
    def form_invalid(self, form):
        print(form.errors)
        if "old_password" in form.errors:
            messages.error(self.request, "Your old password was entered incorrectly. Please enter it again.")
        # elif "new password 2"UeNC8QyQ9
        elif "new_password2" in form.errors:
            messages.error(self.request, "This password is too common.")
        
        error_message = form.get_error(self.request.POST['new_password1'], 
                                       self.request.POST['new_password2']
                                       )
        messages.error(self.request, error_message)
        return super().form_invalid(form)

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

    next_url = request.GET.get('next', dashboard_mapping.get(designation))
    return redirect(next_url, request.user.profile)


def property_single(request):
    form = ContactAgentForm(request.POST if request.method == 'POST' else None)

    if request.method == 'POST' and form.is_valid():
        if not check_network_connection():
            return JsonResponse({"error": "No network connection. Please check your internet."}, status=500)
        
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

    next_url = request.GET.get('next', '/')

    context = {
        'form': form,
        'next_url': next_url,
    }
    return render(request, 'users/property-single.html', context)


def property_grid(request):
    next_url = request.GET.get('next', '/')

    context = {
        'next_url': next_url
    }
    return render(request, 'users/property-grid.html', context)


def blog_single(request):
    next_url = request.GET.get('next', '/')

    context = {
        'next_url': next_url
    }
    return render(request, 'users/blog-single.html', context)


def agents_grid(request):
    next_url = request.GET.get('next', '/')

    context = {
        'next_url': next_url
    }
    return render(request, 'users/agents-grid.html', context)


def agent_single(request):
    next_url = request.GET.get('next', '/')

    context = {
        'next_url': next_url
    }
    return render(request, 'users/agent-single.html', context)


def about(request):
    next_url = request.GET.get('next', '/')

    context = {
        'next_url': next_url
    }
    return render(request, 'users/about.html', context)


def blog(request):
    next_url = request.GET.get('next', '/')

    context = {
        'next_url': next_url
    }
    return render(request, 'users/blog.html', context)


def contact_us(request):
    form = ContactForm(request.POST if request.method == 'POST' else None)

    if request.method == 'POST' and form.is_valid():
        if not check_network_connection():
            return JsonResponse({"error": "No network connection. Please check your internet."}, status=500)
        
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

    next_url = request.GET.get('next', '/')

    context = {
        'form': form,
        'next_url': next_url,
    }
    return render(request, 'users/contact-us.html', context)


def generate_username(first_name, last_name):
    """
    Generates a unique username by combining the first name, last name,
    and a random number. The username is slugified to ensure it's URL-friendly.

    :param first_name: The first name of the client
    :param last_name: The last name of the client
    :return: A unique username string
    """
    # Slugify the names to make them URL-friendly
    base_username = slugify(f"{first_name}{last_name}")

    # Generate a random 4-digit number
    random_number = ''.join(random.choices(string.digits, k=2))

    # Combine the base username with the random number
    username = f"{base_username}{random_number}"

    while User.objects.filter(username=username).exists():
        random_number = ''.join(random.choices(string.digits, k=2))
        username = f"{base_username}{random_number}"

    return username


def generate_password(length=10):
    """
    Generates a random secure password using a combination of letters, digits, and special characters.

    :param length: The length of the password (default is 12 characters)
    :return: A random secure password string
    """
    # Define the character sets to use in the password
    letters = string.ascii_letters  # Includes both lowercase and uppercase letters
    digits = '123456789'  # Includes digits 1-9

    # Combine all character sets
    all_characters = letters + digits

    # Ensure the password includes at least one of each character type
    password = [
        random.choice(letters),
        random.choice(digits),
    ]

    # Fill the rest of the password length with random choices from all characters
    password += random.choices(all_characters, k=length - 3)

    # Shuffle the password list to randomize the order of characters
    random.shuffle(password)

    # Convert the list to a string
    return ''.join(password)


def greet_client():
    current_hour = datetime.now().hour

    if 5 <= current_hour < 12:
        greeting = "Good morning"
    elif 12 <= current_hour < 17:
        greeting = "Good afternoon"
    elif 17 <= current_hour < 21:
        greeting = "Good evening"
    else:
        greeting = "Good night"
    
    return greeting

def check_network_connection():
    try:
        socket.create_connection(("8.8.8.8", 53), timeout=5)
        return True
    except socket.timeout:
        print("Network connection timed out.")
        return False
    except socket.gaierror:
        print("DNS resolution failed.")
        return False
    except OSError as e:
        print(f"Network error: {e}")
        return False
    
def get_activity(request):
    filter_option = request.GET.get('filter', 'all')
    activities = ActivityLog.objects.all()

    # Get the current date
    today = timezone.now().date()

    if filter_option == "all":
        activities = activities.filter(user=request.user) 
    elif filter_option == "28":
        activities = activities.filter(user=request.user, timestamp__gte=timezone.now() - timedelta(days=28))
    elif filter_option == 'last_month':
        first_day_of_current_month = today.replace(day=1)
        last_day_of_previous_month = first_day_of_current_month - timedelta(days=1)
        first_day_of_previous_month = last_day_of_previous_month.replace(day=1)
        activities = activities.filter(user=request.user, timestamp__gte=first_day_of_previous_month, timestamp__lte=last_day_of_previous_month)
    elif filter_option == 'last_year':
        current_year = today.year
        first_day_of_last_year = datetime(current_year - 1, 1, 1).date()
        last_day_of_last_year = datetime(current_year - 1, 12, 31).date()
        activities = activities.filter(user=request.user, timestamp__gte=first_day_of_last_year, timestamp__lte=last_day_of_last_year)

    activities_time = {}
    for activity in activities:
        activity_timestamp = activity.timestamp
        current_time = timezone.now()

        # Subtract the activity timestamp from the current time
        time_difference = current_time - activity_timestamp
        days = time_difference.days
        hours, remainder = divmod(time_difference.seconds, 3600)
        minutes, seconds = divmod(remainder, 60)
        
        if days > 0:
            activities_time[f"{activity.id}"] = [f"{days}", "days" if days > 1 else "day"]
        elif hours > 0:
            activities_time[f"{activity.id}"] = [f"{hours}", "hours" if hours > 1 else "hour"]
        elif minutes > 0:
            activities_time[f"{activity.id}"] = [f"{minutes}", "minutes" if minutes > 1 else "minute"]
        else:
            activities_time[f"{activity.id}"] = [f"{seconds}", "seconds" if seconds > 1 else "second"]

    return activities, activities_time
    