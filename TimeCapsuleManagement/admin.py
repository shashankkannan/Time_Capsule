from django.contrib import admin
from .models import Capsule, CapsuleContent, Subscription, Comment

# Register your models here.
admin.site.register(Capsule)
admin.site.register(CapsuleContent)
admin.site.register(Subscription)
admin.site.register(Comment)
