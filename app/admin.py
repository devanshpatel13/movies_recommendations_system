from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.

@admin.register(MoviesUser)
class MoviesUserAdmin(admin.ModelAdmin):
    list_display = ["id","username", "email", "first_name","first_login"]


@admin.register(MoviesDataBase)
class MoviesAdmin(ImportExportModelAdmin):
    list_display = ['Name',
                    'Year',
                    'Duration',
                    'Rating',
                    'MetaScore',
                    'Vote',
                    'Gross',

                    ]

admin.site.register(SearchMoviesModel)


@admin.register(MoviesDataModel)
class MoviesAdmin(ImportExportModelAdmin):
    list_display = ['budget',
                    'genres',
                    'homepage',
                    'keywords',
                    'original_language',
                    'original_title',
                    'overview',
                    'popularity',
                    'production_companies',
                    'production_countries',
                    'release_date',
                    'revenue',
                    'runtime',
                    'spoken_languages',
                    'status',
                    'tagline',
                    'title',
                    'vote_average',
                    'vote_count',
                    'movie_id',
                    'cast',
                    'crew',


                    ]