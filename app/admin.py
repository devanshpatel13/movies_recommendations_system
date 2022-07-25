from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin
# Register your models here.

@admin.register(MoviesUser)
class MoviesUserAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "first_name","first_login"]


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