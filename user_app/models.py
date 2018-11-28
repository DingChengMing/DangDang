from django.db import models


# Create your models here.
class TUser(models.Model):
    email = models.CharField(max_length=30)
    password = models.CharField(max_length=100)
    username = models.CharField(max_length=20)
    status = models.IntegerField()

    class Meta:
        db_table = 't_user'