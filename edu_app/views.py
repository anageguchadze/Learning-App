from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.models import User
from django.contrib import messages
from .models import Profile, Course, Enrollment
from django.contrib.auth.decorators import login_required
from .forms import CourseForm, EnrollmentForm

def index(request):
    return render(request, 'index.html')

def user_login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            auth_login(request, user)
            profile = get_object_or_404(Profile, user=user)
            if profile.role == 'instructor':
                return redirect('instructor_dashboard')  # Redirect instructors to the dashboard
            elif profile.role == 'student':
                return redirect('student_page')  # Redirect students to their page
            else:
                return redirect('index')  # Redirect to home if role is not defined
        else:
            messages.error(request, 'Invalid credentials')
    return render(request, 'login.html')

def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']
        role = request.POST['role'] 
        
        if password == confirm_password:
            try:
                user = User.objects.create_user(username=username, password=password)
                
                Profile.objects.create(user=user, role=role)
                
                messages.success(request, 'Registration successful! You can now log in.')
                return redirect('login')
            except:
                messages.error(request, 'Username already exists')
        else:
            messages.error(request, 'Passwords do not match')
    
    return render(request, 'register.html')

@login_required
def course_list(request):
    profile = get_object_or_404(Profile, user=request.user)
    if profile.role != 'instructor':
        return redirect('index')  # Redirect non-instructors to home
    courses = Course.objects.filter(instructor=profile)
    return render(request, 'course_list.html', {'courses': courses})

@login_required
def create_course(request):
    profile = get_object_or_404(Profile, user=request.user)
    if profile.role != 'instructor':
        return redirect('index')
    
    if request.method == 'POST':
        form = CourseForm(request.POST)
        if form.is_valid():
            course = form.save(commit=False)
            course.instructor = profile
            course.save()
            messages.success(request, 'Course created successfully!')
            return redirect('course_list')
    else:
        form = CourseForm()
    
    return render(request, 'create_course.html', {'form': form})

@login_required
def update_course(request, course_id):
    profile = get_object_or_404(Profile, user=request.user)
    course = get_object_or_404(Course, id=course_id, instructor=profile)
    
    if request.method == 'POST':
        form = CourseForm(request.POST, instance=course)
        if form.is_valid():
            form.save()
            messages.success(request, 'Course updated successfully!')
            return redirect('course_list')
    else:
        form = CourseForm(instance=course)
    
    return render(request, 'update_course.html', {'form': form})

@login_required
def delete_course(request, course_id):
    profile = get_object_or_404(Profile, user=request.user)
    course = get_object_or_404(Course, id=course_id, instructor=profile)
    
    if request.method == 'POST':
        course.delete()
        messages.success(request, 'Course deleted successfully!')
        return redirect('course_list')
    
    return render(request, 'delete_course.html', {'course': course})

@login_required
def instructor_dashboard(request):
    profile = get_object_or_404(Profile, user=request.user)
    if profile.role != 'instructor':
        return redirect('index')  # Redirect non-instructors to home
    
    courses = Course.objects.filter(instructor=profile)
    return render(request, 'instructor_dashboard.html', {'courses': courses})

@login_required
def student_page(request):
    profile = get_object_or_404(Profile, user=request.user)
    if profile.role != 'student':
        return redirect('index')  # Redirect non-students to home
    
    # Enrolled courses
    enrollments = Enrollment.objects.filter(student=profile)
    courses = Course.objects.filter(id__in=enrollments.values_list('course_id', flat=True))
    
    return render(request, 'student_page.html', {'courses': courses, 'enrollments': enrollments})

@login_required
def enroll_course(request, course_id):
    profile = get_object_or_404(Profile, user=request.user)
    course = get_object_or_404(Course, id=course_id)
    
    if request.method == 'POST':
        Enrollment.objects.get_or_create(student=profile, course=course)
        messages.success(request, 'Enrolled in course successfully!')
        return redirect('student_page')
    
    return render(request, 'enroll_course.html', {'course': course})

@login_required
def update_progress(request, enrollment_id):
    profile = get_object_or_404(Profile, user=request.user)
    enrollment = get_object_or_404(Enrollment, id=enrollment_id, student=profile)
    
    if request.method == 'POST':
        form = EnrollmentForm(request.POST, instance=enrollment)
        if form.is_valid():
            form.save()
            messages.success(request, 'Progress updated successfully!')
            return redirect('student_page')
    else:
        form = EnrollmentForm(instance=enrollment)
    
    return render(request, 'update_progress.html', {'form': form, 'enrollment': enrollment})


@login_required
def available_courses(request):
    profile = get_object_or_404(Profile, user=request.user)
    if profile.role != 'student':
        return redirect('index')  # Redirect non-students to home
    
    # Get all courses excluding those the student is already enrolled in
    enrolled_course_ids = Enrollment.objects.filter(student=profile).values_list('course_id', flat=True)
    available_courses = Course.objects.exclude(id__in=enrolled_course_ids)
    
    return render(request, 'available_courses.html', {'courses': available_courses})