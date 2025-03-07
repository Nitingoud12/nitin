from django.contrib import admin

# Register your models here.
from attendance.models import StudentModel, AttendanceModel, FacultyModel

admin.site.register(StudentModel)
admin.site.register(AttendanceModel)
admin.site.register(FacultyModel)