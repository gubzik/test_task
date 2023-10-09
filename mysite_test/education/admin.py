from django.contrib import admin
from .models import UserProducts, Product, UserLesson, Lesson

# Register your models here.
admin.site.register(UserLesson)
admin.site.register(Product)
admin.site.register(Lesson)
admin.site.register(UserProducts)
