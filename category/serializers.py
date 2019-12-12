from rest_framework import serializers
from rest_framework.fields import SerializerMethodField
from django.contrib.auth.models import User, Group

from .models import Category, Note


class PublicUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email')


class CategorySerializer(serializers.ModelSerializer):
    user = PublicUserSerializer(read_only=True)

    class Meta:
        model = Category
        fields = ('id', 'name', 'user')


class NoteSerializer(serializers.ModelSerializer):
    # serialize the foreign key as an object
    user = PublicUserSerializer(read_only=True)

    class Meta:
        model = Note
        fields = ('id', 'title', 'content'
                  , 'created_at', 'user', 'category')
