from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required, user_passes_test
from django.core.paginator import Paginator
from django.contrib import messages
from django.db.models import Count
from .models import Course, Attendance, Grade
from User.models import CustomUser, StudentProfile, TeacherProfile, SchoolClass, AdminProfile

def is_admin(user):
    return user.is_authenticated and user.role == 'admin'

@login_required
@user_passes_test(is_admin)
def admin_dashboard(request):
    context = {
        'total_students': StudentProfile.objects.count(),
        'total_teachers': TeacherProfile.objects.count(),
        'total_classes': SchoolClass.objects.count(),
        'total_courses': Course.objects.count(),
        'recent_students': StudentProfile.objects.select_related('user', 'student_class').order_by('-id')[:5],
        'recent_teachers': TeacherProfile.objects.select_related('user').order_by('-id')[:5],
    }
    return render(request, 'admin/dashboard.html', context)

@login_required
@user_passes_test(is_admin)
def manage_students(request):
    # Get filters from request
    class_filter = request.GET.get('class')
    search_query = request.GET.get('search')
    
    # Base queryset
    students = StudentProfile.objects.select_related('user', 'student_class')
    
    # Apply filters
    if class_filter:
        students = students.filter(student_class_id=class_filter)
    if search_query:
        students = students.filter(
            Q(user__first_name__icontains=search_query) |
            Q(user__last_name__icontains=search_query) |
            Q(roll_no__icontains=search_query)
        )
    
    # Pagination
    paginator = Paginator(students, 10)  # Show 10 students per page
    page = request.GET.get('page')
    students = paginator.get_page(page)
    
    context = {
        'students': students,
        'classes': SchoolClass.objects.all(),
        'selected_class': class_filter,
        'search_query': search_query,
    }
    return render(request, 'admin/manage_students.html', context)

@login_required
@user_passes_test(is_admin)
def student_detail(request, student_id):
    student = get_object_or_404(StudentProfile.objects.select_related(
        'user', 'student_class'
    ), id=student_id)
    
    context = {
        'student': student,
        'attendance_records': Attendance.objects.filter(student=student).order_by('-date')[:10],
        'grades': Grade.objects.filter(student=student).select_related('course'),
    }
    return render(request, 'admin/student_detail.html', context)

@login_required
@user_passes_test(is_admin)
def student_create(request):
    if request.method == 'POST':
        # Handle form submission
        try:
            # Create user
            user = CustomUser.objects.create_user(
                username=request.POST['username'],
                email=request.POST['email'],
                password=request.POST['password'],
                first_name=request.POST['first_name'],
                last_name=request.POST['last_name'],
                role='student'
            )
            
            # Create student profile
            StudentProfile.objects.create(
                user=user,
                admin_id=request.user.admin_profile,
                roll_no=request.POST['roll_no'],
                student_class_id=request.POST['student_class'],
                guardian_name=request.POST['guardian_name'],
                guardian_contact=request.POST['guardian_contact']
            )
            
            messages.success(request, 'Student created successfully.')
            return redirect('manage_students')
        except Exception as e:
            messages.error(request, f'Error creating student: {str(e)}')
            return redirect('manage_students')
    
    return redirect('manage_students')

@login_required
@user_passes_test(is_admin)
def student_update(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    
    if request.method == 'POST':
        try:
            # Update user
            user = student.user
            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']
            user.email = request.POST['email']
            user.save()
            
            # Update student profile
            student.roll_no = request.POST['roll_no']
            student.student_class_id = request.POST['student_class']
            student.guardian_name = request.POST['guardian_name']
            student.guardian_contact = request.POST['guardian_contact']
            student.save()
            
            messages.success(request, 'Student updated successfully.')
        except Exception as e:
            messages.error(request, f'Error updating student: {str(e)}')
    
    return redirect('student_detail', student_id=student_id)

@login_required
@user_passes_test(is_admin)
def student_delete(request, student_id):
    student = get_object_or_404(StudentProfile, id=student_id)
    
    if request.method == 'POST':
        try:
            user = student.user
            student.delete()
            user.delete()
            messages.success(request, 'Student deleted successfully.')
        except Exception as e:
            messages.error(request, f'Error deleting student: {str(e)}')
    
    return redirect('manage_students')

@login_required
@user_passes_test(lambda u: u.role == 'student')
def student_dashboard(request):
    student = get_object_or_404(StudentProfile, user=request.user)
    
    # Get attendance rate
    total_attendance = Attendance.objects.filter(student=student).count()
    present_attendance = Attendance.objects.filter(student=student, status=True).count()
    attendance_rate = (present_attendance / total_attendance * 100) if total_attendance > 0 else 0
    
    # Get courses and grades
    grades = Grade.objects.filter(student=student).select_related('course', 'course__teacher', 'course__teacher__user')
    
    # Get recent attendance
    recent_attendance = Attendance.objects.filter(student=student).order_by('-date')[:5]
    
    context = {
        'student': student,
        'attendance_rate': round(attendance_rate, 2),
        'total_courses': grades.count(),
        'grades': grades,
        'recent_attendance': recent_attendance,
    }
    return render(request, 'student/dashboard.html', context)
