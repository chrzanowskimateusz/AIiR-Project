from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .forms import RegistrationForm, AccountAuthenticationForm, UploadFileForm


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
            email = request.POST['email']
            password = request.POST['password']
            user = authenticate(email=email, password=password)

            if user:
                login(request, user)
                return redirect("page-tsp")

    else:
        form = AccountAuthenticationForm()

    context['login_form'] = form

    # print(form)
    return render(request, "users/login.html", {'form': form})