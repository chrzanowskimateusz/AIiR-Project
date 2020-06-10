from django.contrib.auth import get_user_model
from django.db import models

user = get_user_model()


class File(models.Model):
    file = models.FileField(default=None, null=True)


class Result(models.Model):
    file_result_path = models.CharField(max_length=240)
    file_result_result = models.CharField(max_length=500)
    file_calculate_time = models.IntegerField()


class CalculatePath(models.Model):
    file_path = models.ForeignKey(File, on_delete=models.CASCADE)
    algorithm = models.CharField(max_length=200)
