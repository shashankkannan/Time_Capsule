from django.contrib import admin
from .models import UserProfile, UserVisit

# Register your models here.
admin.site.register(UserProfile)
admin.site.register(UserVisit)
