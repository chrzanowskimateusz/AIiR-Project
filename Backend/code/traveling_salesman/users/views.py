from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from django.test import RequestFactory
from rest_framework.test import APIClient

from .forms import RegistrationForm, AccountAuthenticationForm, UploadFileForm
from algorithm import models as algorithm_models

def registration_view(request):
    context = {}
    if request.POST:
        form = RegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            email = form.cleaned_data.get('email')
            raw_password = form.cleaned_data.get('password')
            account = authenticate(email=email, password=raw_password)
            login(request, account)
            return redirect('home')
        else:
            context['registration_form'] = form

    else:
        form = RegistrationForm()
        context['registration_form'] = form
    return render(request, 'users/register.html', {'form': form})


def upload_view(request):
    context = {}
    if request.POST:
        form = UploadFileForm(request.POST)
        if form.is_valid():
            form.save()
            factory = RequestFactory()
            content_type = "multipart/form-data"

            factory.post('localhost:8000/upload/')
            return redirect('home')
        else:
            context['file_upload_form'] = form

    else:
        form = UploadFileForm()
        context['file_upload_form'] = form
    return render(request, 'users/upload.html', {'form': form})



def logout_view(request):
    logout(request)
    return redirect('/')


def login_view(request):

    context = {}

    user = request.user
    if user.is_authenticated:
        return redirect("page-tsp")

    if request.POST:
        form = AccountAuthenticationForm(request.POST)
        if form.is_valid():
            username = request.POST['username']
            password = request.POST['password']
            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return redirect("page-tsp")

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    # print(form)
    return render(request, "users/login.html", {'form': form})