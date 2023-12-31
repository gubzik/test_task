from django.contrib import admin
from django.urls import path, include

from education.views import UserProductView, UserProductDetailView, StatisticsView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('<int:user_id>/products/', UserProductView.as_view()),
    path('<int:user_id>/products/<int:product_id>/', UserProductDetailView.as_view()),
    path('statistics/', StatisticsView.as_view()),
]