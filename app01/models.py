from django.db import models

# Create your models here.

class User_Info(models.Model):
    user = models.CharField(max_length=12)
    pwd = models.CharField(max_length=12)
