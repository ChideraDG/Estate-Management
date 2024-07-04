from django.shortcuts import render, redirect
from .forms import RegistrationForm


def register(request):
    form = RegistrationForm()

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
