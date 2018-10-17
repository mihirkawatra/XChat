"""cfehome URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.0/topics/http/urls/
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
from django.urls import reverse_lazy
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView,RedirectView
from chat import views
urlpatterns = [
    path('',RedirectView.as_view(url=reverse_lazy('home'),permanent=False)),
    path('home/', TemplateView.as_view(template_name="chat/home.html"),name='home'),
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.SignUp.as_view(), name='signup'),
    path('admin/', admin.site.urls),
    path('messages/', include('chat.urls')),
]
