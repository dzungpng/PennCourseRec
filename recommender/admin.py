from django.contrib import admin
from .models import Course, SubmittedDescription, SavedDescription

admin.site.register(Course)
admin.site.register(SubmittedDescription)
admin.site.register(SavedDescription)
