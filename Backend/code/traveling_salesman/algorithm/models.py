from django.contrib.auth import get_user_model
from django.db import models

user = get_user_model()


class File(models.Model):
    file_path = models.CharField(max_length=250)
    file_result_path = models.CharField(max_length=250)
    file_result_result = models.IntegerField()
    file_calculate_time = models.IntegerField()
    user = models.ForeignKey(user, on_delete=models.CASCADE)
