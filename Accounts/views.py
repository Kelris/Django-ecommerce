from django.shortcuts import render

# Create your views here.
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import redirect

from .forms import UserCreationForm, AuthenticationForm


def register(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()

            username = form.cleaned_data['username']
            password = form.cleaned_data['password1']
            user = authenticate(username=username, password=password)

            login(request, user)
            return redirect('index')
    else:
        form = UserCreationForm

    context = {'form': form}
    return render(request, 'Accounts/register.html', context)


def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():

            username = form.cleaned_data['username']
            password = form.cleaned_data['password']
            user = authenticate(username=username, password=password)

            login(request, user)

            return redirect('index')
    else:
        form = AuthenticationForm

    context = {'form': form}
    return render(request, 'Accounts/login.html', context)


def change_account(request):
    logout(request)
    if request.method == 'POST':
        register_form = UserCreationForm(request.POST)
        if register_form.is_valid():
            register_form.save()

            username = register_form.cleaned_data['username']
            password = register_form.cleaned_data['password1']

            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('index')

        login_form = AuthenticationForm(data=request.POST)
        if login_form.is_valid():

            username = login_form.cleaned_data['username']
            password = login_form.cleaned_data['password']

            user = authenticate(username=username, password=password)
            login(request, user)

            return redirect('index')

    else:
        register_form = UserCreationForm
        login_form = AuthenticationForm

    context = {'register_form': register_form, 'login_form': login_form}
    return render(request, 'Accounts/change_account.html', context)





