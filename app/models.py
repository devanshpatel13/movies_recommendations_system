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
    search_cast = models.CharField(max_length=500)
    search_crew = models.CharField(max_length=500)
    search_overview = models.CharField(max_length=500 , null=True)
    search_popularity = models.CharField(max_length=500)

    # search_Duration = models.CharField(max_length=500)
    # search_Rating = models.CharField(max_length=500)
    # search_MetaScore = models.CharField(max_length=500)
    # search_Vote = models.CharField(max_length=500)
    # search_Gross = models.CharField(max_length=500)
    search_user = models.CharField(max_length=500)
    search_vote_average = models.CharField(max_length=500)
    search_vote_count = models.CharField(max_length=500)




class MoviesDataModel(models.Model):
    budget = models.CharField(max_length=500)
    genres = models.CharField(max_length=500)
    homepage = models.CharField(max_length=500, null=True)
    # id = models.CharField(max_length=500)
    keywords = models.CharField(max_length=500)
    original_language = models.CharField(max_length=500)
    original_title = models.CharField(max_length=500)
    overview = models.CharField(max_length=500 , null=True)
    popularity = models.CharField(max_length=500)
    production_companies = models.CharField(max_length=500)
    production_countries = models.CharField(max_length=500)
    release_date = models.CharField(max_length=500, null= True)
    revenue = models.CharField(max_length=500)
    runtime = models.CharField(max_length=500 , null= True)
    spoken_languages = models.CharField(max_length=500)
    status = models.CharField(max_length=500)
    tagline = models.CharField(max_length=500, null= True)
    title = models.CharField(max_length=500)
    vote_average = models.CharField(max_length=500)
    vote_count = models.CharField(max_length=500)
    movie_id = models.CharField(max_length=500)
    cast = models.CharField(max_length=1000)
    crew = models.CharField(max_length=1000)