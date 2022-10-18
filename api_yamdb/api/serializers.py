from rest_framework import serializers
from rest_framework.relations import SlugRelatedField

from reviews.models import Genre, Categories, Title


class GenreSerializer(serializers.ModelSerializer):

    class Meta:
        model = Genre
        fields = ('name', 'slug')


class CategoriesSerializer(serializers.ModelSerializer):

    class Meta:
        model = Categories
        fields = ('name', 'slug')


class TittleSerializer(serializers.ModelSerializer):
    genre = SlugRelatedField(slug_field='slug', read_only=True, many=True)
    category = SlugRelatedField(slug_field='slug', read_only=True)

    class Meta:
        model = Title
        fields = ('id', 'name', 'year', 'description', 'genre', 'category')
