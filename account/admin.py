from django.contrib import admin

# Register your models here.
from .models import UserData, Team

admin.site.register(UserData)
admin.site.register(Team)
