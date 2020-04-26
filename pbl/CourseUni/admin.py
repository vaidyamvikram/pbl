from django.contrib import admin
from .models import courses,categories,teacher,mycourses
# Register your models here.
admin.site.register(courses)
admin.site.register(categories)
admin.site.register(teacher)
admin.site.register(mycourses)