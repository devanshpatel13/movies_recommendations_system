import csv
import pandas as pd
from django.db.models import Q
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, CreateAPIView
from rest_framework import status
from app.models import *
from email_validator import validate_email, EmailNotValidError, caching_resolver
from app.serializers import RegisterSerializer, MoviesDataSerializers
from app.tests import get_recommendations, cosine_sim2


class CreateView(CreateAPIView):
    queryset = MoviesUser.objects.all()
    serializer_class = RegisterSerializer


    def post(self, request, *args, **kwargs):
        email = request.data["email"]
        serializer = self.serializer_class(data=request.data)
        if request.data["password"] != request.data["confirm_password"]:
            return Response({"msg": "password and confirm password does not match"},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            if email:
                #Resolve the cashing issues if any
                resolver = caching_resolver(timeout=10)
                try:
                    #Validate email address and domain address (pypi:"https://pypi.org/project/email-validator/")
                    email = validate_email(email, dns_resolver=resolver).email
                except EmailNotValidError as e:
                    return Response({
                        "msg": "Either email domain does not exist or the format of the email is not proper"},
                        status=status.HTTP_400_BAD_REQUEST)
                except Exception as e:
                    return Response({
                        "msg": "Something went wrong!"},
                        status=status.HTTP_400_BAD_REQUEST)
            get_user = MoviesUser.objects.get(username=request.data['username'])
            return Response({"msg": f'username {get_user} is already exit'})
        except Exception as e:
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data)
            return Response({"msg":"not valid"})

'''
Call only once for fetching data from the dataset and import it to our database.
'''
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


class MoviesDetails(ListAPIView):
    queryset = MoviesDataModel.objects.all()
    serializer_class = MoviesDataSerializers

    def filter_queryset(self, params):
        filter_kwargs = {}

        if "search" in params:
            query = Q(title__icontains=params['search'])

        return self.queryset.filter(query)


    def get(self, request, *args, **kwargs):

        if request.query_params.copy():
            if (list(request.query_params.copy().keys())[0]) == 'search':
                if ("search" in request.query_params.copy()) and (request.query_params.copy()['search'] != ''):
                    self.params = request.query_params.copy()
                    queryset = self.filter_queryset(self.params)
                    data = MoviesDataSerializers(queryset, many=True).data
                    if data:
                        for x in data:
                            """
                            save movies search history when user searches any movies 
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
                        return Response({'message': "This movie doesn't exist"},
                                        status=status.HTTP_200_OK)

                else:
                    if request.user.first_login == False:
                        """
                        Check user first_login status and give suggestion based on rating if first_login is Flase
                        """
                        get_top10_movies = MoviesDataModel.objects.filter().order_by("-vote_average")[:10]
                        data = MoviesDataSerializers(get_top10_movies, many=True).data
                        if data:
                            request.user.first_login = True
                            request.user.save()
                        return Response(data, status=status.HTTP_200_OK)
                    else:
                        list1 = []
                        set1 = set()
                        list2 = []

                        movies = SearchMoviesModel.objects.filter(search_user=request.user.pk).values()
                        """
                        get searched movies and give movies suggestions based on user search history
                        """
                        if movies:
                            for x in movies:
                                get_search_movies_name = x['search_movie_name']
                                set1.add(get_search_movies_name)
                                list2 = list(set1)
                            for data in list2:
                                y = get_recommendations(data, cosine_sim2)
                                list1.append(y)

                            aa = list1
                            return Response(aa, status=status.HTTP_302_FOUND)
                        else:
                            get_top10_movies = MoviesDataModel.objects.filter().order_by("-vote_average")[:10]
                            data = MoviesDataSerializers(get_top10_movies, many=True).data
                            return Response(data, status=status.HTTP_200_OK)
            else:
                # get_top10_movies = MoviesDataModel.objects.filter().order_by("-vote_average")[:10]
                # data = MoviesDataSerializers(get_top10_movies, many=True).data
                # return Response(data, status=status.HTTP_200_OK)

                return Response({'message': "url doesn't exist"},
                                status=status.HTTP_200_OK)
        else:
            list1 = []
            set1 = set()
            list2 = []

            movies = SearchMoviesModel.objects.filter(search_user=request.user.pk).values()
            if movies:
                for x in movies:
                    """
                    give movies suggestions based on user search history
                    """
                    get_search_movies_name = x['search_movie_name']
                    set1.add(get_search_movies_name)
                    list2 = list(set1)
                for data in list2:
                    y = get_recommendations(data, cosine_sim2)
                    list1.append(y)
                suggestion_movies = list1
                return Response(suggestion_movies, status=status.HTTP_302_FOUND)
            else:

                """
                give suggestions based on rating 
                """
                get_top10_movies = MoviesDataModel.objects.filter().order_by("-vote_average")[:10]
                data = MoviesDataSerializers(get_top10_movies, many=True).data
                return Response(data, status=status.HTTP_200_OK)

