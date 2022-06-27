from rest_framework import serializers
from .models import *
from django.contrib.auth.hashers import make_password
from rest_framework.response import Response
from rest_framework import status

class UserNetListSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserNet
        fields = ('email', 'age', 'gender')


class UserNetDetailSerializer(serializers.ModelSerializer):

    class Meta:
        model = UserNet
        fields = ('email', 'age', 'telephone', 'gender')


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)
    def create(self, validated_data):
        user = UserNet.objects.create_user(**validated_data)
        return user
    class Meta:
        model = UserNet
        fields = ('age', 'description', 'telephone', 'email', 'gender', 'password')

class ImageDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostImages
        fields = ("image", 'description')

class PostNetDetailSerializer(serializers.ModelSerializer):
    postimages = ImageDetailSerializer(read_only=True)

    class Meta:
        model = PostNet
        fields = ('title', 'content', 'photo', 'postimages', 'time_create',)

class PostNetUpdateSerializer(serializers.ModelSerializer):
    postimages = ImageDetailSerializer(write_only=True)

    class Meta:
        model = PostNet
        fields = ('title', 'content', 'postimages', 'time_create',) #'author', 
    def create(self, validated_data):
        validated_data.pop('postimages', None)
        return super().create(validated_data)


class FilterOneSerializers(serializers.Serializer):
    user = UserNetDetailSerializer(read_only=True)
    posts = PostNetDetailSerializer(read_only=True)

class FilterManysSerializers(serializers.Serializer):
    user = UserNetDetailSerializer(read_only=True)
    posts = PostNetDetailSerializer(read_only=True, many=True)

class PostUpdateOneSerializer(serializers.Serializer):
    post = PostNetDetailSerializer(read_only=True)
    images = ImageDetailSerializer(read_only=True)

class PostUpdateManySerializer(serializers.Serializer):
    post = PostNetDetailSerializer(read_only=True)
    images = ImageDetailSerializer(read_only=True, many=True)