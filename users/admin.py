from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Mentor, Seeker

admin.site.register(Mentor)
admin.site.register(Seeker)
