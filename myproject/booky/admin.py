from django.contrib import admin
from .models import (Book, Order, Teacher, Grade,
                     Classroom, OwnedByTeacher, OwnedByClass)

admin.site.register(Book)
admin.site.register(Order)
admin.site.register(Teacher)
admin.site.register(Grade)
admin.site.register(Classroom)
admin.site.register(OwnedByTeacher)
admin.site.register(OwnedByClass)
