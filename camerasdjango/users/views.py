from django.urls import reverse_lazy
from django.views.generic import CreateView
from .forms import CustomUserCreationForm
from django.views.generic import ListView
from .models import CustomUser
from django.shortcuts import render
from django_tables2 import RequestConfig,tables




#class UserManagementView(ListView):
#	model = CustomUser
#	template_name = 'user_management.html'
#	context_object_name = 'all_users_list'


class UsersTable(tables.Table):
    class Meta:
        model = CustomUser
        
        template_name = 'django_tables2/bootstrap.html'
        exclude = ['password','is_superuser','id','email','is_staff','edad']
        sequence=['username','first_name','last_name','cargo','is_active','...']
       
        

def UserManagementView(request):
    table = UsersTable(CustomUser.objects.all())
 

    RequestConfig(request).configure(table)
    return render(request, 'users/user_management.html', {'table': table})

class SignUpView(CreateView):
	form_class = CustomUserCreationForm
	success_url = reverse_lazy('home')
