from django.urls import path, include 
from .views import UserManagementView
from users.forms import CustomAuthenticationForm 
from django.contrib.auth import views as auth_views
from users.views import SignUpView
from django.conf.urls import url
from django.conf import settings
from django.contrib.auth import logout

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(authentication_form=CustomAuthenticationForm), name='login'),
    path('signup/', SignUpView.as_view(template_name='users/signup.html'), name='signup'),
    path('', include('django.contrib.auth.urls')), 
    path('user_management/', UserManagementView, name='user_management'),
    url(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout')
]