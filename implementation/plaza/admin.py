from django.contrib import admin
from plaza.models import Course
from plaza.models import Person
from plaza.models import Notification

# Register your models here.
admin.site.register(Course)
admin.site.register(Person)
admin.site.register(Notification)

