from rest_framework import serializers
from .models import *
from rest_framework.response import Response


class RegisterSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})
    password = serializers.CharField(write_only=True, required=True, style={"input_type": "password"})
    username = serializers.CharField(max_length=15)
    first_name = serializers.CharField(max_length=15)

    class Meta:
        model = MoviesUser
        fields = ['username', 'email', 'password', 'confirm_password', 'first_name']


    # def validate(self, attrs ,code= None, detail=None):
    #     if attrs['password'] != attrs['confirm_password']:
    #         raise serializers.ValidationError({"password": "Password fields didn't match."})
    #     return attrs

    def create(self, validated_data):
        user = MoviesUser.objects.create(
            username=validated_data['username'],
            email=validated_data['email'],
            first_name=validated_data['first_name'],
        )
        user.set_password(validated_data['password'])
        user.save()
        return user


class MoviesSearchSerializers(serializers.ModelSerializer):
    class Meta:
        model = SearchMoviesModel
        fields = "__all__"


class MoviesDataSerializers(serializers.ModelSerializer):
    class Meta:
        model = MoviesDataModel
        fields = "__all__"
