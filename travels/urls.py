from django.contrib import admin
from django.urls import path

from .views import indexView

app_name = 'travels'

urlpatterns = [
    path('', indexView, name = 'index'),
    path('admin/', admin.site.urls),
]
