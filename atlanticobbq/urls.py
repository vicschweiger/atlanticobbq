"""
URL configuration for atlanticobbq project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from reservations import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.index, name='index'),
    path('submit/', views.submit_login, name='submit_login'),
    path('calendar/', views.calendar_view, name='calendar'),
    path('edit_user/', views.edit_user, name='edit_user'),
    path('edit_reservations/', views.edit_reservations, name='edit_reservations'),
    path('edit_reservations/submit/', views.submit_reservations, name='submit_reservation'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),    
]
