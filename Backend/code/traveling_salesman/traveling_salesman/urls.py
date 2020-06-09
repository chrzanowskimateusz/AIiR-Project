"""traveling_salesman URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path
from users import api_views as user_views
from algorithm import api_views as algorithm_views
from django.conf import settings
from django.conf.urls import url, include
from rest_framework import routers
from users.views import (
    registration_view,
    login_view,
    logout_view,
    upload_view,
)

urlpatterns = [

    url('admin/', admin.site.urls),
    url('register/', registration_view, name='register'),
    url('logout/', logout_view, name='logout'),
    url('login/', login_view, name='login'),
    url('home/', upload_view, name='home'),
    path('results/', algorithm_views.Results.as_view(), name='page-history'),
    path('upload/', algorithm_views.FileUpload.as_view(), name='page-tsp'),
    path('userResults/', algorithm_views.UserResults.as_view(), name='page-profile'),

    #REST API
    url('', include('rest_framework.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

