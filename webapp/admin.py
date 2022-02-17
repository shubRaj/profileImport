from django.contrib import admin
from .models import CSVModel
@admin.register(CSVModel)
class AdminCSVModel(admin.ModelAdmin):
    list_display = ("full_name","date_of_birth","added_by","added_on")
    search_fields = ("full_name",)
    list_filter = ("added_by","date_of_birth",)
    date_hierarchy = 'added_on'