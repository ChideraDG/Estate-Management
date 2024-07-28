from django.shortcuts import render, redirect
from .forms import CompanyForm
from .models import Company


def createCompany(request):
    form = CompanyForm()
    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()

            return redirect('company-home')

    context = {'form': form}
    return render(request, 'companies/companyRegistration.html', context)


def companyHome(request):
    profiles = Company.objects.all()

    context = {'profiles': profiles}
    return render(request, 'companies/companyHome.html', context)


def updateCompany(request, pk):
    try:
        profile = Company.objects.get(id=pk)
    except Company.DoesNotExist:
        return redirect('custom_404')

    form = CompanyForm(instance=profile)

    if request.method == 'POST':
        form = CompanyForm(request.POST, request.FILES, instance=profile)

        if form.is_valid():
            form.save()

            return redirect('company-home')

    context = {'form': form, 'profile': profile}
    return render(request, 'companies/updateCompany.html', context)


def viewCompany(request, pk):
    company = Company.objects.get(id=pk)

    context = {'company': company}
    return render(request, 'companies/viewCompany.html', context)


def deleteCompany(request, pk):
    profile = Company.objects.get(id=pk)

    if request.method == 'POST':
        profile.delete()
        return redirect('company-home')

    context = {'obj': profile}
    return render(request, 'companies/deleteCompany.html', context)
