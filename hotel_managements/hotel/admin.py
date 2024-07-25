from django.contrib import admin
from .models import CustomUser,Hotel
# Register your models here.
admin.site.register(CustomUser)
admin.site.register(Hotel)