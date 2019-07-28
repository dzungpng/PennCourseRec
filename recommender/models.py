from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User

class Course(models.Model):
    name = models.TextField(null=True)
    number = models.TextField(null=True)
    description = models.TextField(null=True)
    course_quality = models.TextField(null=True)
    difficulty = models.TextField(null=True)

    def __str__(self):
        return self.name

class SubmittedDescription(models.Model):
    user = models.ForeignKey(User, null = True, blank = True, on_delete = models.DO_NOTHING)
    description = models.TextField(null = True)
    name = models.CharField(max_length=200)
    created_date = models.DateTimeField(default=timezone.now)
