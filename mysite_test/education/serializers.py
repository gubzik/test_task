from django.contrib.auth import get_user_model
from rest_framework import serializers
from .models import Product, UserLesson, UserProducts, Lesson

from django.contrib.auth import get_user_model

User = get_user_model()


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'pk']


class UserLessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = UserLesson
        fields = ['id', 'status', 'watched_time', 'last_time_watched']


class LessonSerializer(serializers.ModelSerializer):
    userlesson_set = UserLessonSerializer(many=True, read_only=True)

    class Meta:
        model = Lesson
        fields = ['id', 'title', 'video_link', 'duration', 'userlesson_set']


class ProductSerializer(serializers.ModelSerializer):
    lesson_set = LessonSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = ['title', 'owner', 'lesson_set']


class UserProductSerializer(serializers.ModelSerializer):
    product = ProductSerializer()

    class Meta:
        model = UserProducts
        fields = ['user', 'product']
