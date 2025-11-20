"""
URL configuration for ocmsproject project.
"""
from django.contrib import admin
from django.urls import path, include
from . import views

urlpatterns = [
    path('admin/', admin.site.urls),
    path("", views.homefunction, name="home"),
    path("demo", views.demofunction1, name="demo1"),
    path("demo1", views.demofunction2, name="demo2"),
    path("home", views.homefunction, name="home"),
    path("about", views.aboutfunction, name="about"),
    path("login", views.loginfunction, name="login"),
    path("contact", views.contactfunction, name="contact"),
    path("", include("adminapp.urls")),
    path("", include("studentapp.urls")),
    path("", include("instructorapp.urls")),
]
