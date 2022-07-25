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

from app.serializers import RegisterSerializer, MovieSerializer, MoviesSearchSerializers


# Create your views here.

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
    stu = MoviesDataBase.objects.all()
    data = []
    for s in stu:
        data.append({
            'Name': s.Name,
            'Year': s.Year,
            'Duration': s.Duration,
            'Rating': s.Rating,
            'MetaScore': s.MetaScore,
            'Vote': s.Vote,
            'Gross': s.Gross,

        })
    pd.DataFrame(data).to_excel('data.xlsx', index=False)
    excel = pd.read_excel('data.xlsx', index_col=0)
    print(excel)
    return JsonResponse({'status': 200})


class MoviesDetails(ListCreateAPIView):
    queryset = MoviesDataBase.objects.all()
    serializer_class = MovieSerializer


    def filter_queryset(self, params):
        # import pdb;pdb.set_trace()
        filter_kwargs = {}
        if "search" in params:
            query = Q(Name=params['search'])

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
        data = MovieSerializer(queryset, many= True).data
        for x in data:
            Search = SearchMoviesModel.objects.create(
                search_Name=x['Name'],
                search_Year=x['Year'],
                search_Duration=x['Duration'],
                search_Rating=x['Rating'],
                search_MetaScore=x['MetaScore'],
                search_Vote=x['Vote'],
                search_Gross=x['Gross'],
                search_user=request.user.username

            )
            Search.save()



        if request.user.first_login == False:
            """
            Check useis first time login , then give output on rating based
            """

            get_top10_movies = MoviesDataBase.objects.filter().order_by("-Rating")[:10]
            data = MovieSerializer(get_top10_movies, many=True).data

            if data:
                request.user.first_login = True
                request.user.save()
                return Response(data, status=status.HTTP_302_FOUND)

        else:
            pass
            # get_search_movies = MoviesDataBase.objects.all()
            # search_data = MovieSerializer(get_search_movies, many=True).data
            # return Response(search_data, status=status.HTTP_302_FOUND)

            # print("ddddddddddddddddddddddddddd")
        return Response(data, status=status.HTTP_200_OK)
