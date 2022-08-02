from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.


class MoviesUser(AbstractUser):
    first_login = models.BooleanField(default=False)


# To Remove
class MoviesDataBase(models.Model):
    Name = models.CharField(max_length=500)
    Year = models.CharField(max_length=500)
    Duration = models.CharField(max_length=500)
    Rating = models.CharField(max_length=500)
    MetaScore = models.CharField(max_length=500)
    Vote = models.CharField(max_length=500)
    Gross = models.CharField(max_length=500)


class SearchMoviesModel(models.Model):
    search_movie_name = models.TextField()
    search_movie_date = models.TextField(blank= True, null=True)
    search_movie_cast = models.TextField()
    search_movie_crew = models.TextField()
    search_movie_overview = models.TextField(max_length=500, null=True)
    search_movie_popularity = models.BigIntegerField()
    search_user = models.ForeignKey(MoviesUser,on_delete=models.CASCADE, blank=True, null=True)
    search_movie_vote_average = models.BigIntegerField()
    search_movie_vote_count = models.BigIntegerField()


class MoviesDataModel(models.Model):
    budget = models.FloatField()
    genres = models.TextField()
    homepage = models.TextField(null=True)
    # id = models.CharField(max_length=500)
    keywords = models.TextField()
    original_language = models.TextField()
    original_title = models.TextField()
    overview = models.TextField(null=True)
    popularity = models.FloatField()
    production_companies = models.TextField()
    production_countries = models.TextField()
    release_date = models.TextField(blank=True, null=True)
    revenue = models.BigIntegerField()
    runtime = models.BigIntegerField(null=True)
    spoken_languages = models.TextField()
    status = models.BigIntegerField()
    '''(1=> Released ,2=>Rumored, 3=>Post Production)'''
    tagline = models.TextField(null= True)
    title = models.TextField()
    vote_average = models.BigIntegerField()
    vote_count = models.BigIntegerField()
    movie_id = models.BigIntegerField()
    cast = models.TextField()
    crew = models.TextField()
