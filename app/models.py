from django.db import models
from django.contrib.auth.models import User,AbstractUser

# Create your models here.


class MoviesUser(AbstractUser):
    first_login = models.BooleanField(default=False)




class MoviesDataBase(models.Model):
    Name = models.CharField(max_length=500)
    Year = models.CharField(max_length=500)
    Duration = models.CharField(max_length=500)
    Rating = models.CharField(max_length=500)
    MetaScore = models.CharField(max_length=500)
    Vote = models.CharField(max_length=500)
    Gross = models.CharField(max_length=500)

