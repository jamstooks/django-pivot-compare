from django.db import models
from djongo import models as djongo_models


class CourseScore(models.Model):

    course_name = models.CharField(max_length=4)
    student_name = models.CharField(max_length=16)
    score = models.IntegerField()

    # the manager for postgres
    objects = models.Manager()
    # the djongo manager for mongodb
    mobjects = djongo_models.DjongoManager()
