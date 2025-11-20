from django.urls import path
from . import views

urlpatterns = [
    path("studentlogincheck", views.studentlogincheck, name="studentlogincheck"),
    path("studenthome", views.studenthome, name="studenthome"),
    path("studentlogout", views.studentlogout, name="studentlogout"),
    path("availablecourses", views.availablecourses, name="availablecourses"),
    path("enrollcourse/<int:course_id>", views.enrollcourse, name="enrollcourse"),
    path("studentcourses", views.studentcourses, name="studentcourses"),
]