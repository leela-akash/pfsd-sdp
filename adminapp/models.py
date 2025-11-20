from django.db import models

# Create your models here.
class Admin(models.Model):
    id=models.AutoField(primary_key=True)
    username=models.CharField(max_length=100,blank=False,unique=True)
    password=models.CharField(max_length=100,blank=False)

    class Meta:
        db_table="admin_table"
        
class Course(models.Model):
    id=models.AutoField(primary_key=True)
    department = models.CharField(max_length=100)
    academicyear = models.CharField(max_length=20, blank=False)
    semester = models.CharField(max_length=10, blank=False)
    year = models.IntegerField(blank=False)
    coursecode=models.CharField(max_length=20,blank=False)
    coursetitle = models.CharField(max_length=100, blank=False)
    credits = models.IntegerField(default=3)
    instructor_id = models.BigIntegerField(null=True, blank=True)
    
    class Meta:
        db_table="course_table"
        
    def __str__(self):
        return f"{self.coursecode} - {self.coursetitle}"
        
class Student(models.Model):
    id=models.AutoField(primary_key=True)
    studentid=models.BigIntegerField(blank=False,unique=True)
    fullname=models.CharField(max_length=100,blank=False)
    gender=models.CharField(max_length=20,blank=False)
    department=models.CharField(max_length=50,blank=False)
    program = models.CharField(max_length=50, blank=False)
    semester = models.CharField(max_length=10, blank=False)
    year = models.IntegerField(blank=False)
    password=models.CharField(max_length=100,blank=False,default="Akash")
    email=models.CharField(max_length=100,blank=False,unique=True)
    contact=models.CharField(max_length=20,blank=False,unique=True)

    class Meta:
        db_table = "student_table"
        
    def __str__(self):
        return f"{self.fullname} ({self.studentid})"

class Instructor(models.Model):
    id = models.AutoField(primary_key=True)
    instructorid = models.BigIntegerField(blank=False, unique=True)
    fullname = models.CharField(max_length=100, blank=False)
    gender = models.CharField(max_length=20, blank=False)
    department = models.CharField(max_length=50, blank=False)
    qualification = models.CharField(max_length=50, blank=False)
    designation = models.CharField(max_length=50, blank=False)
    password = models.CharField(max_length=100, blank=False, default="Akash")
    email = models.CharField(max_length=100, blank=False, unique=True)
    contact = models.CharField(max_length=20, blank=False, unique=True)

    class Meta:
        db_table = "instructor_table"
        
    def __str__(self):
        return f"{self.fullname} ({self.instructorid})"

class Enrollment(models.Model):
    id = models.AutoField(primary_key=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='enrollments')
    course = models.ForeignKey(Course, on_delete=models.CASCADE, related_name='enrollments')
    enrollment_date = models.DateTimeField(auto_now_add=True)
    grade = models.CharField(max_length=5, null=True, blank=True)
    
    class Meta:
        db_table = "enrollment_table"
        unique_together = ['student', 'course']
        
    def __str__(self):
        return f"{self.student.fullname} - {self.course.coursetitle}"
