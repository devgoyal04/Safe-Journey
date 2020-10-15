from django.contrib import admin
from django.urls import path
from django.contrib.auth.views import LogoutView
from .views import indexView, dashboard, register, loginView, booking, bookingDetails

app_name = 'travels'

urlpatterns = [
    path('', indexView, name = 'index'),
    path('register/',register, name='register'),
    path('dashboard/', dashboard, name = 'dashboard'),
    path('booking/<src>/<dest>/<date>', booking, name = 'booking'),
    path('details/<src>/<dest>/<train>/<date>', bookingDetails, name = 'bookingDetails'),
    path('login/', loginView, name='login'),
    path('logout/', LogoutView.as_view(next_page='travels:index'), name='logout'),
]
