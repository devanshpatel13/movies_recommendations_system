from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from .views import *

#
# from rest_framework import routers
#
# router = routers.DefaultRouter()
# router.register("create", CreateView , basename = "create")
# router.register("moviesdetails", MoviesDetails , basename = "moviesdetails")

urlpatterns = [

    path('', CreateView.as_view(), name="create"),
    path("movies/", MoviesdataView, name="movies"),
    path("movies_details/", MoviesDetails.as_view(), name="moviesdetails"),
    path('auth', include('rest_framework.urls', namespace='rest_framework'))

]
