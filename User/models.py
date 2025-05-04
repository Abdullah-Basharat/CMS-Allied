from django.db import models
from django.contrib.auth.models import AbstractUser
from datetime import datetime


# Create your models here.
class CustomUser(AbstractUser):
    """
    Custom user model that extends the default Django user model.
    """
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('student', 'Student'),
        ('teacher', 'Teacher'),
    )
    Gender_CHOICES = (
        ('male',"Male"),
        ('female',"Female"),
        ('other',"Other"),
    )

    role = models.CharField(choices=ROLE_CHOICES, max_length=10, default='student')
    gender = models.CharField(choices=Gender_CHOICES,max_length=10,null=True,blank=True)
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    def __str__(self):
        return self.username

class AdminProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='admin_profile')

    def __str__(self):
        return self.user.username

class SchoolClass(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True)
    admin_id = models.ForeignKey(AdminProfile, on_delete=models.CASCADE, related_name='admin_classes')
    def __str__(self):
        return self.name


class TeacherProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='teacher_profile')
    admin = models.ForeignKey(AdminProfile, on_delete=models.CASCADE, related_name='admin_teachers')
    employee_id = models.CharField(max_length=20, unique=True)
    specialization = models.CharField(max_length=100)
    hire_date = models.DateField(default=datetime.now)
    class_id = models.ForeignKey(SchoolClass, on_delete=models.CASCADE, related_name='teacher_classes',null=True,blank=True)  # Assuming Class model exists
    class_assiging_time = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.user.username

class StudentProfile(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='student_profile')
    admin_id = models.ForeignKey(AdminProfile, on_delete=models.CASCADE, related_name='admin_students')
    roll_no = models.CharField(max_length=20)
    date_of_birth = models.DateField(null=True, blank=True)
    guardian_name = models.CharField(max_length=100, blank=True)
    guardian_contact = models.CharField(max_length=15, blank=True)
    student_class = models.ForeignKey(SchoolClass, on_delete=models.SET_NULL, null=True)  # Uncomment if Class model exists

    def __str__(self):
        return self.user.username