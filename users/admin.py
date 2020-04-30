from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Advisor, Users

admin.site.register(Advisor)
admin.site.register(Users)
