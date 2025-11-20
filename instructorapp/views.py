from django.shortcuts import render, redirect
from django.contrib import messages
from adminapp.models import Instructor, Course, Enrollment

# Create your views here.

def instructorlogincheck(request):
    if request.method == 'POST':
        instructorid = request.POST.get('instructorid')
        password = request.POST.get('password')
        
        try:
            instructor = Instructor.objects.get(instructorid=instructorid, password=password)
            request.session['instructor_id'] = instructor.id
            request.session['role'] = 'instructor'
            request.session['instructor_name'] = instructor.fullname
            messages.success(request, f'Welcome {instructor.fullname}!')
            return redirect('instructorhome')
        except Instructor.DoesNotExist:
            messages.error(request, 'Invalid credentials!')
            return redirect('login')
    return redirect('login')

def instructorlogout(request):
    if 'role' in request.session:
        del request.session['role']
    if 'instructor_id' in request.session:
        del request.session['instructor_id']
    if 'instructor_name' in request.session:
        del request.session['instructor_name']
    messages.info(request, 'Logged out successfully!')
    return redirect('login')

def instructorhome(request):
    if 'role' not in request.session or request.session['role'] != 'instructor':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    instructor = Instructor.objects.get(id=request.session['instructor_id'])
    courses = Course.objects.filter(instructor_id=instructor.id)
    
    context = {
        'instructor': instructor,
        'courses_count': courses.count(),
    }
    return render(request, 'instructor/instructorhome.html', context)

def instructorcourses(request):
    if 'role' not in request.session or request.session['role'] != 'instructor':
        messages.error(request, 'Please login first!')
        return redirect('login')
    
    instructor = Instructor.objects.get(id=request.session['instructor_id'])
    courses = Course.objects.filter(instructor_id=instructor.id)
    
    # Get enrollments for each course
    course_details = []
    for course in courses:
        enrollments = Enrollment.objects.filter(course=course)
        course_details.append({
            'course': course,
            'enrollment_count': enrollments.count(),
            'enrollments': enrollments,
        })
    
    context = {
        'course_details': course_details,
        'instructor': instructor,
    }
    return render(request, 'instructor/instructorcourses.html', context)


def instructoraddcourse(request):
    if 'role' not in request.session or request.session['role'] != 'instructor':
        messages.error(request, 'Please login first!')
        return redirect('login')

    instructor = Instructor.objects.get(id=request.session['instructor_id'])

    if request.method == 'POST':
        department = request.POST.get('department')
        academicyear = request.POST.get('academicyear')
        semester = request.POST.get('semester')
        year = request.POST.get('year')
        coursecode = request.POST.get('coursecode')
        coursetitle = request.POST.get('coursetitle')
        credits = request.POST.get('credits', 3)

        # Basic validation for numeric fields
        try:
            year = int(year)
            credits = int(credits)
        except (TypeError, ValueError):
            messages.error(request, 'Year and Credits must be numeric values.')
            return render(request, 'instructor/addcourse.html', {'instructor': instructor})

        try:
            Course.objects.create(
                department=department,
                academicyear=academicyear,
                semester=semester,
                year=year,
                coursecode=coursecode,
                coursetitle=coursetitle,
                credits=credits,
                instructor_id=instructor.id
            )
            messages.success(request, 'Course created successfully!')
            return redirect('instructorcourses')
        except Exception as exc:
            messages.error(request, f'Error creating course: {exc}')

    return render(request, 'instructor/addcourse.html', {'instructor': instructor})