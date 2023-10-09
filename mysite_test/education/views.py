from django.shortcuts import render
from django.db.models import Prefetch, Q, Count, Sum
from rest_framework.generics import ListAPIView, RetrieveAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import UserProducts, Lesson, UserLesson, Product
from .serializers import UserProductSerializer
from django.contrib.auth import get_user_model
from datetime import timedelta
import re

User = get_user_model()


class StatisticsView(APIView):

    def get(self, request):
        result = []
        products_list = Product.objects.all().prefetch_related('userproducts_set').prefetch_related(
            'lesson_set__userlesson_set')
        if len(products_list) == 0:
            raise ValidationError(detail={"detail": "Products doesn't exist"})
        total_users = User.objects.all().count()

        for product in products_list:
            obj = {}
            obj['product_id'] = product.pk
            obj['product'] = product.title
            obj['count_students'] = product.userproducts_set.all().count()

            count = 0
            for lesson in product.lesson_set.all():
                for userlesson in lesson.userlesson_set.all():
                    if userlesson.status == 'Просмотрено':
                        count += 1
            obj['count_of_watched_lessons'] = count

            time_spent = timedelta()
            for lesson in product.lesson_set.all():
                for userlesson in lesson.userlesson_set.all():
                    time_spent += userlesson.watched_time
            obj['time_spent'] = time_spent

            obj['percent'] = (
                f"{product.userproducts_set.all().count() / total_users}"
            )

            result.append(obj)

        return Response(data=result, status=status.HTTP_200_OK)


class UserProductView(ListAPIView):
    queryset = UserProducts.objects.none()
    serializer_class = UserProductSerializer

    def get_queryset(self):
        user_id = self.kwargs['user_id']

        userlesson = UserLesson.objects.filter(user__id=user_id)
        queryset = (
            UserProducts.objects.filter(user__id=user_id)
            .prefetch_related(Prefetch('product__lesson_set__userlesson_set',
                                       queryset=userlesson))
        )

        return queryset


class UserProductDetailView(RetrieveAPIView):
    queryset = UserProducts.objects.none()
    serializer_class = UserProductSerializer

    def get_object(self):
        user_id = self.kwargs['user_id']
        product_id = self.kwargs['product_id']
        userlesson = UserLesson.objects.filter(user__id=user_id)
        obj = (
            UserProducts.objects.filter(user__id=user_id, product__id=product_id)
            .prefetch_related(Prefetch('product__lesson_set__userlesson_set',
                                       queryset=userlesson))
        )
        if len(obj) == 0:
            raise ValidationError(detail={'detail': 'incorrect_product_id'})
        return obj[0]