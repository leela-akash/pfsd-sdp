from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from .models import Admin, Student, Instructor, Course, Enrollment
import hashlib

# Create your views here.

def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()

# Authentication Views
def adminlogincheck(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        try:
            admin = Admin.objects.get(username=username, password=password)
            request.session['admin_id'] = admin.id
            request.session['role'] = 'admin'
            messages.success(request, 'Login successful!')
            return redirect('adminhome')
        except Admin.DoesNotExist:
            messages.error(request, 'Invalid credentials!')
            return redirect('login')
    return redirect('login')

def logout(request):
    if 'role' in request.session:
        del request.session['role']
    if 'admin_id' in request.session:
        del request.session['admin_id']
    messages.info(request, 'Logged out successfully!')
    return redirect('login')

# Dashboard
def adminhome(request):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    # Get statistics
    total_students = Student.objects.count()
    total_instructors = Instructor.objects.count()
    total_courses = Course.objects.count()
    total_enrollments = Enrollment.objects.count()
    
    context = {
        'total_students': total_students,
        'total_instructors': total_instructors,
        'total_courses': total_courses,
        'total_enrollments': total_enrollments,
    }
    return render(request, 'admin/adminhome.html', context)

# Student CRUD
def addstudent(request):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    if request.method == 'POST':
        studentid = request.POST.get('studentid')
        fullname = request.POST.get('fullname')
        gender = request.POST.get('gender')
        department = request.POST.get('department')
        program = request.POST.get('program')
        semester = request.POST.get('semester')
        year = request.POST.get('year')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('password', 'Akash')
        
        try:
            Student.objects.create(
                studentid=studentid, fullname=fullname, gender=gender,
                department=department, program=program, semester=semester,
                year=year, email=email, contact=contact, password=password
            )
            messages.success(request, 'Student added successfully!')
            return redirect('allstudents')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'admin/addstudent.html')

def allstudents(request):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    students = Student.objects.all()
    return render(request, 'admin/allstudents.html', {'students': students})

def editstudent(request, student_id):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    student = get_object_or_404(Student, id=student_id)
    
    if request.method == 'POST':
        student.studentid = request.POST.get('studentid')
        student.fullname = request.POST.get('fullname')
        student.gender = request.POST.get('gender')
        student.department = request.POST.get('department')
        student.program = request.POST.get('program')
        student.semester = request.POST.get('semester')
        student.year = request.POST.get('year')
        student.email = request.POST.get('email')
        student.contact = request.POST.get('contact')
        student.save()
        messages.success(request, 'Student updated successfully!')
        return redirect('allstudents')
    
    return render(request, 'admin/editstudent.html', {'student': student})

def deletestudent(request, student_id):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    student = get_object_or_404(Student, id=student_id)
    student.delete()
    messages.success(request, 'Student deleted successfully!')
    return redirect('allstudents')

# Instructor CRUD
def addinstructor(request):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    if request.method == 'POST':
        instructorid = request.POST.get('instructorid')
        fullname = request.POST.get('fullname')
        gender = request.POST.get('gender')
        department = request.POST.get('department')
        qualification = request.POST.get('qualification')
        designation = request.POST.get('designation')
        email = request.POST.get('email')
        contact = request.POST.get('contact')
        password = request.POST.get('password', 'Akash')
        
        try:
            Instructor.objects.create(
                instructorid=instructorid, fullname=fullname, gender=gender,
                department=department, qualification=qualification, designation=designation,
                email=email, contact=contact, password=password
            )
            messages.success(request, 'Instructor added successfully!')
            return redirect('allinstructors')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'admin/addinstructor.html')

def allinstructors(request):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    instructors = Instructor.objects.all()
    return render(request, 'admin/allinstructors.html', {'instructors': instructors})

def editinstructor(request, instructor_id):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    instructor = get_object_or_404(Instructor, id=instructor_id)
    
    if request.method == 'POST':
        instructor.instructorid = request.POST.get('instructorid')
        instructor.fullname = request.POST.get('fullname')
        instructor.gender = request.POST.get('gender')
        instructor.department = request.POST.get('department')
        instructor.qualification = request.POST.get('qualification')
        instructor.designation = request.POST.get('designation')
        instructor.email = request.POST.get('email')
        instructor.contact = request.POST.get('contact')
        instructor.save()
        messages.success(request, 'Instructor updated successfully!')
        return redirect('allinstructors')
    
    return render(request, 'admin/editinstructor.html', {'instructor': instructor})

def deleteinstructor(request, instructor_id):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    instructor = get_object_or_404(Instructor, id=instructor_id)
    instructor.delete()
    messages.success(request, 'Instructor deleted successfully!')
    return redirect('allinstructors')

# Course CRUD
def addcourse(request):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    instructors = Instructor.objects.all()
    
    if request.method == 'POST':
        department = request.POST.get('department')
        academicyear = request.POST.get('academicyear')
        semester = request.POST.get('semester')
        year = request.POST.get('year')
        coursecode = request.POST.get('coursecode')
        coursetitle = request.POST.get('coursetitle')
        credits = request.POST.get('credits', 3)
        instructor_id = request.POST.get('instructor_id')
        
        try:
            Course.objects.create(
                department=department, academicyear=academicyear, semester=semester,
                year=year, coursecode=coursecode, coursetitle=coursetitle,
                credits=credits, instructor_id=instructor_id
            )
            messages.success(request, 'Course added successfully!')
            return redirect('allcourses')
        except Exception as e:
            messages.error(request, f'Error: {str(e)}')
    
    return render(request, 'admin/addcourse.html', {'instructors': instructors})

def allcourses(request):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    courses = Course.objects.all()
    return render(request, 'admin/allcourses.html', {'courses': courses})

def editcourse(request, course_id):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    course = get_object_or_404(Course, id=course_id)
    instructors = Instructor.objects.all()
    
    if request.method == 'POST':
        course.department = request.POST.get('department')
        course.academicyear = request.POST.get('academicyear')
        course.semester = request.POST.get('semester')
        course.year = request.POST.get('year')
        course.coursecode = request.POST.get('coursecode')
        course.coursetitle = request.POST.get('coursetitle')
        course.credits = request.POST.get('credits', 3)
        course.instructor_id = request.POST.get('instructor_id')
        course.save()
        messages.success(request, 'Course updated successfully!')
        return redirect('allcourses')
    
    return render(request, 'admin/editcourse.html', {'course': course, 'instructors': instructors})

def deletecourse(request, course_id):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    course = get_object_or_404(Course, id=course_id)
    course.delete()
    messages.success(request, 'Course deleted successfully!')
    return redirect('allcourses')

# View Enrollments
def viewenrollments(request):
    if 'role' not in request.session or request.session['role'] != 'admin':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    enrollments = Enrollment.objects.select_related('student', 'course').all()
    return render(request, 'admin/viewenrollments.html', {'enrollments': enrollments})
