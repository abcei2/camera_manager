from django.http import HttpResponseRedirect
from django.urls import reverse
from django.contrib.auth import authenticate, login, logout
from django.template import RequestContext
from django.shortcuts import render


def home(request):
    return HttpResponseRedirect(reverse('cameras:manage_cameras'))


def login_user(request):
    logout(request)
    email = password = ''
    if request.POST:
        email = request.POST['email']
        password = request.POST['password']

        user = authenticate(email=email, password=password)
        if user is not None:
            if user.is_active:
                login(request, user)
                return HttpResponseRedirect('/')
    return render(request, 'registration/login.html', context={'errors': True})
