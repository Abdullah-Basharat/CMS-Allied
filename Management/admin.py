from django.contrib import admin

from .models import Course, Attendance, Grade
from User.models import SchoolClass

admin.site.register(SchoolClass)
admin.site.register(Course)
admin.site.register(Attendance)
admin.site.register(Grade)


