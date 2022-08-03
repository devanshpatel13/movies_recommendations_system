# import APIResponse as APIResponse
import json
import pdb
from django.db.models import Q
from .paginations import *
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
from rest_framework.generics import ListAPIView, CreateAPIView, get_object_or_404
from rest_framework import status
from app.models import *

from app.serializers import RegisterSerializer, MoviesDataSerializers, MoviesSearchSerializers

# Create your views here.
from app.tests import get_recommendations, cosine_sim2


class CreateView(CreateAPIView):
    queryset = MoviesUser.objects.all()
    serializer_class = RegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        # import pdb;pdb.set_trace()
        try:
            get_user = MoviesUser.objects.get(username=request.data['username'])
            return Response({"msg": f'username {get_user} is already exit'})
        except Exception as e:
            if serializer.is_valid():
                serializer.save()
            return Response(serializer.data)


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
    # pd.DataFrame(data).to_excel('/home/plutusdev/Downloads/test.xlsx', index=False)
    # excel = pd.read_excel('/home/plutusdev/Downloads/test.xlsx', index_col=0)
    # print(excel)
    return JsonResponse({'status': 200})


class MoviesDetails(ListAPIView):
    queryset = MoviesDataModel.objects.all()
    serializer_class = MoviesDataSerializers
    pagination_class = Pagenations


    def filter_queryset(self, params):
        # import pdb;pdb.set_trace()
        filter_kwargs = {}

        if "search" in params:
            query = Q(title__icontains=params['search'])

        return self.queryset.filter(query)

    def get(self, request, *args, **kwargs):


        # self.params=  request.query_params.copy()
        # page_size = self.params.get('page_size', None)
        # page = self.params.get('page', None)
        # self.validate_quet
        """
    For the search
        """

        # super().get()
        # import pdb;pdb.set_trace()
        if request.query_params.copy():
            if (list(request.query_params.copy().keys())[0]) == 'search':
                if ("search" in request.query_params.copy()) and (request.query_params.copy()['search'] != ''):
                    self.params = request.query_params.copy()
                    queryset = self.filter_queryset(self.params)
                    data = MoviesDataSerializers(queryset, many=True).data
                    if data:
                        for x in data:
                            """
                            save user search history
                            """
                            Search = SearchMoviesModel.objects.create(
                                search_movie_name=x['title'],
                                search_movie_date=x['release_date'],
                                search_movie_cast=x['cast'],
                                search_movie_crew=x['crew'],
                                search_movie_overview=x['overview'],
                                search_movie_popularity=x['popularity'],
                                search_movie_vote_average=x['vote_average'],
                                search_movie_vote_count=x['vote_count'],
                                search_user=request.user

                            )
                            Search.save()
                        return Response(data, status=status.HTTP_200_OK)
                    else:
                        # get_top10_movies = MoviesDataModel.objects.filter().order_by("-vote_average")[:10]
                        # data = MoviesDataSerializers(get_top10_movies, many=True).data
                        # return Response(data, status= status.HTTP_200_OK)
                        '''
                        OR 
                        '''
                        return Response({'message': "This movie doesn't exist", 'status_code': status.HTTP_200_OK})

                else:
                    if request.user.first_login == False:
                        """
                        Check user first_login status and give suggestion based on rating if first_login == Flase"""
                        get_top10_movies = MoviesDataModel.objects.filter().order_by("-vote_average")[:10]
                        data = MoviesDataSerializers(get_top10_movies, many=True).data
                        if data:
                            request.user.first_login = True
                            request.user.save()
                        return Response(data, status=status.HTTP_200_OK)
                    else:
                        lsd = []
                        st = set()
                        lst = []

                        """
                        give movies suggestions based on user search history
                         """

                        movies = SearchMoviesModel.objects.filter(search_user=request.user.pk).values()
                        if movies:
                            # pdb.set_trace()
                            for x in movies:
                                get_search_movies_name = x['search_movie_name']
                                st.add(get_search_movies_name)
                                lst = list(st)
                            for data in lst:
                                y = get_recommendations(data, cosine_sim2)
                                lsd.append(y)
                            aa = lsd
                            return Response(aa, status=status.HTTP_302_FOUND)
                        else:
                            get_top10_movies = MoviesDataModel.objects.filter().order_by("-vote_average")[:10]
                            data = MoviesDataSerializers(get_top10_movies, many=True).data
                            return Response(data, status=status.HTTP_200_OK)
            else:
                get_top10_movies = MoviesDataModel.objects.filter().order_by("-vote_average")[:10]
                data = MoviesDataSerializers(get_top10_movies, many=True).data
                page = self.paginate_queryset(get_top10_movies)

                if page is not None:
                    serializer = self.get_serializer(page, many=True)
                    return self.get_paginated_response(serializer.data)

                return Response(data, status=status.HTTP_200_OK)

        #         return Response({'message': "url doesn't exist", 'status_code': 200})
        else:
            lsd = []
            st = set()
            lst = []
            """
            give movies suggestions based on user search history
             """
            movies = SearchMoviesModel.objects.filter(search_user=request.user.pk).values()
            if movies:
                for x in movies:
                    get_search_movies_name = x['search_movie_name']
                    st.add(get_search_movies_name)
                    lst = list(st)
                for data in lst:
                    y = get_recommendations(data, cosine_sim2)
                    lsd.append(y)
                aa = lsd
                return Response(aa, status=status.HTTP_302_FOUND)
            else:
                get_top10_movies = MoviesDataModel.objects.filter().order_by("-vote_average")[:10]
                data = MoviesDataSerializers(get_top10_movies, many=True).data
                return Response(data, status=status.HTTP_200_OK)

                # return Response(data, status=status.HTTP_200_OK)

                # return Response("ssssssssssssssssss")

            # print(request.user.first_login, "ddddddddddddddddddddddd")
            # import pdb; pdb.set_trace()

        # print(request.user.id)
        # import pdb;pdb.set_trace()
        # data = MoviesDataSerializers(queryset, many= True).data
        # print(data,"gggggggggggggggg")
        # for x in data:
        #     Search = SearchMoviesModel.objects.create(
        #         search_movie_name=x['title'],
        #         search_movie_date=x['release_date'],
        #         search_movie_cast=x['cast'],
        #         search_movie_crew=x['crew'],
        #         search_movie_overview=x['overview'],
        #         search_movie_popularity=x['popularity'],
        #         search_movie_vote_average=x['vote_average'],
        #         search_movie_vote_count=x['vote_count'],
        #         search_user=request.user
        #
        #     )
        #     Search.save()

        # print(request.user.first_login, "ddddddddddddddddddddddd")

        # if request.user.first_login == False:
        #     print(request.user.first_login,"llllllllllllllllllll")
        #
        #     """
        #     Check if user first time login , then give output based on movies rating
        #     """
        #
        #     get_top10_movies = MoviesDataModel.objects.filter().order_by("-vote_average")[:10]
        #     data = MoviesDataSerializers(get_top10_movies, many=True).data
        #
        #
        #     if data:
        #         request.user.first_login = True
        #         request.user.save()
        #     return Response(data, status=status.HTTP_302_FOUND)
        #
        # else:
        #     if data:
        #         return Response(data, status= status.HTTP_302_FOUND)
        #     else:
        #         print(request.user.first_login, "ddddddddddddddddddddddd")

        # lsd =[]
        # st = set()
        # lst = []
        # """
        # give movies suggestions based on user search history
        #  """
        #
        # # import pdb; pdb.set_trace()
        # movies = SearchMoviesModel.objects.filter(search_user=request.user.pk).values()
        #
        # print(movies,"gggggggggggggggggggggg")
        # if movies:
        #     for x in movies:
        #         get_search_movies_name = x['search_movie_name']
        #         print(get_search_movies_name,"ssssssssssssssssssssssssssssssssssssssssssssssss")
        #         st.add(get_search_movies_name)
        #
        #         lst =list(st)
        #
        #     print(lst)
        #     # import pdb;pdb.set_trace()
        #     for data in lst:
        #         y = get_recommendations(data, cosine_sim2)
        #         lsd.append(y)
        #
        #     print(get_search_movies_name,"@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
        #     aa = lsd
        #     print(aa)
        #     return Response(aa, status=status.HTTP_302_FOUND)
        # else:
        #     get_top10_movies = MoviesDataModel.objects.filter().order_by("-vote_average")[:10]
        #     data = MoviesDataSerializers(get_top10_movies, many=True).data
        #     return Response(data, status=status.HTTP_200_OK)

        # return Response(data,status=status.HTTP_200_OK)
