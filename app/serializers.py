from rest_framework import serializers
from .models import *
from rest_framework.response import Response
from rest_framework.validators import UniqueValidator

from django.shortcuts import get_object_or_404


class RegisterSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})
    password = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})
    username = serializers.CharField(max_length=15)
    first_name = serializers.CharField(max_length=15)

    class Meta:
        model = MoviesUser
        fields = ['username', 'email', 'password', 'password2', 'first_name']

    def validate(self, attrs):
        print(attrs)
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
