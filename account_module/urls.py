from django.urls import path
from account_module import views

urlpatterns = [
    path('login', views.LoginView.as_view(), name='login'),
]
