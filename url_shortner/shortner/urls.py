"""
URL configuration for url_shortner project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from shortner.views import *

urlpatterns = [
     path('', home, name='home'),  #
    path('shorturls/', create_short_url, name='create'), 
    path('shorturls/<str:shortcode>/', get_stats, name='analytics'),  
    path('<str:shortcode>/', redirect_view, name='redirect'),
]


