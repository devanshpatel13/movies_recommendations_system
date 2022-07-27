# import APIResponse as APIResponse
import json

from django.db.models import Q
from django.shortcuts import render

# Create your views here.
import csv

import pandas as pd
# from django.contrib.auth.models import User
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
# from requests import Response
from rest_framework.filters import SearchFilter
from rest_framework.request import Request
from rest_framework.response import Response
from rest_framework import viewsets
from rest_framework.generics import ListCreateAPIView
from rest_framework import status
from app.models import *

from app.serializers import RegisterSerializer, MoviesDataSerializers, MoviesSearchSerializers


# Create your views here.
from app.tests import get_recommendations, cosine_sim2


class CreateView(ListCreateAPIView):
    queryset = MoviesUser.objects.all()
    serializer_class = RegisterSerializer
    # def list(self, request, *args, **kwargs):
    #
    #
    #     return (request,*args)


def MoviesdataView(request):

    """
    import and export data to data
    """
    stu = MoviesDataModel.objects.all()
    data = []
    for s in stu:
        data.append({
            'budget': s.budget,
            'genres': s.genres,
            'homepage': s.homepage,
            'keywords': s.keywords,
            'original_language': s.original_language,
            'original_title': s.original_title,
            'overview': s.overview,
            'popularity': s.popularity,
            'production_companies': s.production_companies,
            'production_countries': s.production_countries,
            'release_date': s.release_date,
            'revenue': s.revenue,
            'runtime': s.runtime,
            'spoken_languages': s.spoken_languages,
            'status': s.status,
            'tagline': s.tagline,
            'title': s.title,
            'vote_average': s.vote_average,
            'vote_count': s.vote_count,
            'movie_id': s.movie_id,
            'cast': s.cast,
            'crew': s.crew,

        })
    pd.DataFrame(data).to_excel('/home/plutusdev/Downloads/test.xlsx', index=False)
    excel = pd.read_excel('/home/plutusdev/Downloads/test.xlsx', index_col=0)
    print(excel)
    return JsonResponse({'status': 200})


class MoviesDetails(ListCreateAPIView):
    queryset = MoviesDataModel.objects.all()
    serializer_class = MoviesDataSerializers


    def filter_queryset(self, params):
        # import pdb;pdb.set_trace()
        filter_kwargs = {}
        if "search" in params:
            query = Q(title=params['search'])

        return self.queryset.filter(query)

    def get(self, request, *args, **kwargs):

        """
    FOr the search
    """
        self.params = request.query_params.copy()
        print(self.params)
        queryset = self.filter_queryset(self.params)
        print(queryset,"++++++++++++++++++++++++++++++++++++")
        print(request.user, "ddddddddddddddddddddddd")
        # import pdb; pdb.set_trace()
        '''
        save user search data 
        '''
        data = MoviesDataSerializers(queryset, many= True).data
        for x in data:
            Search = SearchMoviesModel.objects.create(
                search_Name=x['title'],
                search_Year=x['release_date'],
                search_cast=x['cast'],
                search_crew=x['crew'],
                search_overview=x['overview'],
                search_popularity=x['popularity'],
                search_vote_average=x['vote_average'],
                search_vote_count=x['vote_count'],
                search_user=request.user.id

            )
            Search.save()



        if request.user.first_login == False:

            """
            Check if user first time login , then give output on rating based
            """

            get_top10_movies = MoviesDataModel.objects.filter().order_by("-Rating")[:10]
            data = MoviesDataSerializers(get_top10_movies, many=True).data


            if data:
                request.user.first_login = True
                request.user.save()
                return Response(data, status=status.HTTP_302_FOUND)

        else:
            ...

            # import pdb;pdb.set_trace()
            # data = SearchMoviesModel.objects.get(id=id).filter("search_Name")
            # print(data,"sssssssssssssssssssssss")
            movies = SearchMoviesModel.objects.filter(search_user=3).values()
            for x in movies:
                get_search_movies_name = x['search_Name']
                y = get_recommendations(get_search_movies_name, cosine_sim2)
                print(get_search_movies_name,"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")

                print(y,">>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>")
            print('args ========== ', self.params.values())
            import pdb;pdb.set_trace()
            print(request.user.search_Name,"gggggggggggggg")
            for x in self.params.values():

               y= get_recommendations(x, cosine_sim2)
            # import pdb; pdb.set_trace()
            ...
            return Response(y, status=status.HTTP_302_FOUND)


        return Response(data,status=status.HTTP_200_OK)
