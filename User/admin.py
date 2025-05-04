from django.contrib import admin

# Register your models here.
from .models import CustomUser, TeacherProfile, StudentProfile,AdminProfile


admin.site.register(CustomUser)
admin.site.register(AdminProfile)
admin.site.register(TeacherProfile)
admin.site.register(StudentProfile)
