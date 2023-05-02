from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView

from .forms import LoginForm

from . import views

app_name = 'users'

urlpatterns = [
    path('signup/', views.RetisterView.as_view(), name='signup'),
    path('login/', LoginView.as_view(
        template_name='users/login.html',
        authentication_form=LoginForm,
        redirect_authenticated_user=True
        ), name='login'),
    path('logout/', LogoutView.as_view(
        template_name='users/logout.html',
        ), name='logout'),
]
