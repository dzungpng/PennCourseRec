from django.db import models

class Course(models.Model):
    name = models.TextField(null=True)
    number = models.TextField(null=True)
    description = models.TextField(null=True)
    course_quality = models.TextField(null=True)
    difficulty = models.TextField(null=True)

    def __str__(self):
        return self.name
