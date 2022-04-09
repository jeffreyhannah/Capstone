from django.contrib import admin

# Register your models here.

from django.contrib import admin
from .models import uploadFile


@admin.register(uploadFile)
class UploadAdmin(admin.ModelAdmin):
	list_display = ['user', 'file_field']
