from django.urls import path
from . import views

urlpatterns = [
    # Authentication
    path("adminlogincheck", views.adminlogincheck, name="adminlogincheck"),
    path("adminhome", views.adminhome, name="adminhome"),
    path("adminlogout", views.logout, name="adminlogout"),
    
    # Student CRUD
    path("addstudent", views.addstudent, name="addstudent"),
    path("allstudents", views.allstudents, name="allstudents"),
    path("editstudent/<int:student_id>", views.editstudent, name="editstudent"),
    path("deletestudent/<int:student_id>", views.deletestudent, name="deletestudent"),
    
    # Instructor CRUD
    path("addinstructor", views.addinstructor, name="addinstructor"),
    path("allinstructors", views.allinstructors, name="allinstructors"),
    path("editinstructor/<int:instructor_id>", views.editinstructor, name="editinstructor"),
    path("deleteinstructor/<int:instructor_id>", views.deleteinstructor, name="deleteinstructor"),
    
    # Course CRUD
    path("addcourse", views.addcourse, name="addcourse"),
    path("allcourses", views.allcourses, name="allcourses"),
    path("editcourse/<int:course_id>", views.editcourse, name="editcourse"),
    path("deletecourse/<int:course_id>", views.deletecourse, name="deletecourse"),
    
    # Enrollments
    path("viewenrollments", views.viewenrollments, name="viewenrollments"),
]