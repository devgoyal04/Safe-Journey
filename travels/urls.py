from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import indexView,dashboard,register

app_name = 'travels'

urlpatterns = [
    path('', indexView, name = 'index'),
    path('register/',register, name='register'),
    path('dashboard/', dashboard, name = 'dashboard'),
    path('login/', LoginView.as_view(redirect_authenticated_user=True), name='login'),
    path('logout/', LogoutView.as_view(next_page='travels:index'), name='logout'),
]
