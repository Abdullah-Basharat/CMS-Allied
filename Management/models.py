from django.db import models
from User.models import TeacherProfile,StudentProfile,AdminProfile,SchoolClass
from datetime import datetime



class Course(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    admin_id = models.ForeignKey(AdminProfile, on_delete=models.CASCADE, related_name='admin_courses')
    teacher = models.ForeignKey(TeacherProfile, on_delete=models.CASCADE, related_name='teacher_courses')
    # students = models.ManyToManyField(StudentProfile, related_name='courses', blank=True)
    class_id = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='courses')  # Assuming Class model exists
    total_marks = models.IntegerField(default=100)  # Total marks for the course

    def __str__(self):
        return self.name


class Attendance(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    class_id = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='attendance_records')
    date = models.DateField(default=datetime.now)
    status = models.BooleanField(default=True)  # True for present, False for absent

    def __str__(self):
        return f"{self.student.user.username} - {self.date} - {'Present' if self.status else 'Absent'}"


class Grade(models.Model):
    student = models.ForeignKey(StudentProfile, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
    first_term_marks = models.IntegerField(default=0)
    second_term_marks = models.IntegerField(default=0)
    final_marks = models.IntegerField(default=0)

    def __str__(self):
        return f"{self.student.user.username} - {self.course.name} - {self.grade}"
