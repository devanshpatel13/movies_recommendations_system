import datetime

from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers
from rest_framework.validators import UniqueValidator
from .models import *

from django.utils import timezone


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True)

    class Meta:
        model = MoviesUser
        fields = ['username', 'email', 'password', 'password2', 'first_name','first_login']

    def validate(self, attrs):
        if attrs['password'] != attrs['password2']:
            raise serializers.ValidationError({"password": "Password fields didn't match."})

        return attrs

    def create(self, validated_data):
        user = MoviesUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],

        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class MovieSerializer(serializers.ModelSerializer):
    class Meta:
        model = MoviesDataBase
        fields = "__all__"




class MoviesSearchSerializers(serializers.ModelSerializer):
    class Meta:
        model = SearchMoviesModel
        fields = "__all__"

class MoviesDataSerializers(serializers.ModelSerializer):
    class Meta:
        model = MoviesDataModel
        fields = "__all__"

    # def search_create(self, validated_data,):
        # import pdb;
        # pdb.set_trace()

        # Search = SearchMoviesModel.objects.create(
        #     search_Name=validated_data['Name'],
        #     search_Year=validated_data['Year'],
        #     search_Duration=validated_data['Duration'],
        #     search_Rating = validated_data['Rating'],
        #     search_MetaScore= validated_data['MetaScore'],
        #     search_Vote= validated_data['Vote'],
        #     search_Gross= validated_data['Gross'],
        #     search_user = validated_data["request.user"]
        #
        # )
        # Search.save()


