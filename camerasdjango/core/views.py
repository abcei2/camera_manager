from django.http import HttpResponseRedirect
from django.urls import reverse


def home(request):
    return HttpResponseRedirect(reverse('cameras:manage_cameras'))
