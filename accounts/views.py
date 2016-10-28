from django.shortcuts import render, redirect

from accounts.forms import LoginForm, RegistrationForm
from django.contrib.auth import login as django_login, authenticate, logout as django_logout

from tradenity.sdk.entities import Customer


def login(request):
    if request.method == 'POST':
        form = LoginForm(data=request.POST)
        if form.is_valid():
            user = authenticate(
                username=form.cleaned_data['username'],
                password=form.cleaned_data['password'])
            if user is not None and user.is_active:
                django_login(request, user)
                if 'next_url' in request.session:
                    next_url = request.session['next_url']
                    del request.session['next_url']
                    request.session.modified = True
                    return redirect(next_url)
                else:
                    return redirect('/')
    else:
        if 'next' in request.GET:
            request.session['next_url'] = request.GET['next']
        form = LoginForm()
    return render(request, 'accounts/login.html', {'form': form})


def register(request):
    if request.method == 'POST':
        form = RegistrationForm(data=request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            customer = Customer(firstName=cd['first_name'], lastName=cd['last_name'], email=cd['email'],
                                username=cd['username'], password=cd['password'])
            customer.create()
            return redirect('/accounts/login')
    else:
        form = RegistrationForm()
    return render(request, 'accounts/register.html', {'form': form})


def logout(request):
    django_logout(request)
    return redirect('/')
