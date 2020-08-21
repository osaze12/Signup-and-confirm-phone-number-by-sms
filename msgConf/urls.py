"""msgConf URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
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
from confBySms import views

urlpatterns = [
    path('admin/', admin.site.urls),

    path('create', views.create_profile, name="create"),
    path('confirmToken', views.confirm_token, name="confirm_token"),
    path('process', views.process, name='process'),
    path('reset', views.resend_token, name='reset'),

    path('login', views.login, name='login')
]
