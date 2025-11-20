from django.shortcuts import render, redirect
from django.contrib import messages
from adminapp.models import Student, Course, Enrollment

def studentlogincheck(request):
    if request.method == 'POST':
        studentid = request.POST.get('studentid')
        password = request.POST.get('password')
        
        try:
            student = Student.objects.get(studentid=studentid, password=password)
            request.session['student_id'] = student.id
            request.session['role'] = 'student'
            request.session['student_name'] = student.fullname
            messages.success(request, f'Welcome {student.fullname}!')
            return redirect('studenthome')
        except Student.DoesNotExist:
            messages.error(request, 'Invalid credentials!')
            return redirect('login')
    return redirect('login')

def studentlogout(request):
    if 'role' in request.session:
        del request.session['role']
    if 'student_id' in request.session:
        del request.session['student_id']
    if 'student_name' in request.session:
        del request.session['student_name']
    messages.info(request, 'Logged out successfully!')
    return redirect('login')

def studenthome(request):
    if 'role' not in request.session or request.session['role'] != 'student':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    student = Student.objects.get(id=request.session['student_id'])
    enrolled_courses = Enrollment.objects.filter(student=student)
    
    context = {
        'student': student,
        'enrolled_count': enrolled_courses.count(),
    }
    return render(request, 'student/studenthome.html', context)

def availablecourses(request):
    if 'role' not in request.session or request.session['role'] != 'student':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    student = Student.objects.get(id=request.session['student_id'])
    enrolled_course_ids = Enrollment.objects.filter(student=student).values_list('course_id', flat=True)
    available_courses = Course.objects.exclude(id__in=enrolled_course_ids)
    
    context = {
        'courses': available_courses,
        'student': student,
    }
    return render(request, 'student/availablecourses.html', context)

def enrollcourse(request, course_id):
    if 'role' not in request.session or request.session['role'] != 'student':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    student = Student.objects.get(id=request.session['student_id'])
    course = Course.objects.get(id=course_id)
    
    # Check if already enrolled
    if Enrollment.objects.filter(student=student, course=course).exists():
        messages.warning(request, 'You are already enrolled in this course!')
        return redirect('studentcourses')
    
    Enrollment.objects.create(student=student, course=course)
    messages.success(request, f'Successfully enrolled in {course.coursetitle}!')
    return redirect('studentcourses')

def studentcourses(request):
    if 'role' not in request.session or request.session['role'] != 'student':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    student = Student.objects.get(id=request.session['student_id'])
    enrollments = Enrollment.objects.filter(student=student)
    
    context = {
        'enrollments': enrollments,
        'student': student,
    }
    return render(request, 'student/studentcourses.html', context)
