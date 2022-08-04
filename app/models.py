from django.db import models
from django.contrib.auth.models import User, AbstractUser

# Create your models here.


class MoviesUser(AbstractUser):
    first_login = models.BooleanField(default=False)


class SearchMoviesModel(models.Model):
    search_user = models.ForeignKey(MoviesUser, on_delete=models.CASCADE, blank=True, null=True)
    search_movie_popularity = models.BigIntegerField()
    search_movie_vote_average = models.BigIntegerField()
    search_movie_vote_count = models.BigIntegerField()
    search_movie_name = models.TextField()
    search_movie_date = models.TextField(blank=True, null=True)
    search_movie_cast = models.TextField()
    search_movie_crew = models.TextField()
    search_movie_overview = models.TextField(max_length=500, null=True)


class MoviesDataModel(models.Model):
    movie_id = models.BigIntegerField()
    vote_average = models.BigIntegerField()
    vote_count = models.BigIntegerField()
    revenue = models.BigIntegerField()
    runtime = models.BigIntegerField(null=True)
    status = models.IntegerField()
    '''(1=> Released ,2=>Rumored, 3=>Post Production)'''
    budget = models.FloatField()
    popularity = models.FloatField()
    genres = models.TextField()
    homepage = models.TextField(null=True)
    keywords = models.TextField()
    original_language = models.TextField()
    original_title = models.TextField()
    overview = models.TextField(null=True)
    production_companies = models.TextField()
    production_countries = models.TextField()
    release_date = models.TextField(blank=True, null=True)
    spoken_languages = models.TextField()
    tagline = models.TextField(null=True)
    title = models.TextField()
    cast = models.TextField()
    crew = models.TextField()
