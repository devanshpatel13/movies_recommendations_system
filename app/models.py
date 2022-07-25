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



class SearchMoviesModel(models.Model):
    search_Name = models.CharField(max_length=500)
    search_Year = models.CharField(max_length=500)
    search_Duration = models.CharField(max_length=500)
    search_Rating = models.CharField(max_length=500)
    search_MetaScore = models.CharField(max_length=500)
    search_Vote = models.CharField(max_length=500)
    search_Gross = models.CharField(max_length=500)
    search_user = models.CharField(max_length=500)