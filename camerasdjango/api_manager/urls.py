from django.urls import path
from django.http import HttpResponse

from rest_framework.authtoken.views import obtain_auth_token

from api_manager.views import HelloView

urlpatterns = [
    path('', HelloView.as_view()),
    path('get-token/', obtain_auth_token, name='api_token_auth'),
]
