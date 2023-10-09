from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Product(models.Model):
    """
    Модель продуктов
    """
    title = models.CharField(max_length=255)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Продукт'
        verbose_name_plural = 'Продукты'

    def __str__(self) -> str:
        return f"{self.title}"


class UserProducts(models.Model):
    """
    Модель отношения продуктов и пользователей
    """
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)

    class Meta:
        verbose_name = 'Продукт пользователя'
        verbose_name_plural = 'Продукты пользователей'
        unique_together = ['user', 'product']

    def __str__(self) -> str:
        return f"pk-{self.pk}, User-{self.user.username}"


class Lesson(models.Model):
    """
    Модель уроков
    """
    product = models.ManyToManyField(Product, blank=True)
    title = models.CharField(max_length=128)
    video_link = models.URLField()
    duration = models.DurationField(blank=True, null=True)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'
        ordering = ('duration',)

    def __str__(self) -> str:
        return f"{self.title} - {self.video_link} - {self.duration}"


class UserLesson(models.Model):
    """
    Модель отношения уроков пользователя
    """

    watched_time = models.DurationField(default=0)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    lesson = models.ForeignKey(Lesson, on_delete=models.CASCADE)
    last_time_watched = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=30, blank=True)

    class Meta:
        unique_together = ['user', 'lesson']
        verbose_name = 'Урок пользователя'
        verbose_name_plural = 'Уроки пользователей'

    def __str__(self) -> str:
        return f"pk-{self.pk}"

    def save(self, *args, **kwargs) -> None:
        if self.watched_time >= self.lesson.duration * 0.8:
            self.status = 'Просмотрено'
        else:
            self.status = 'Не просмотрено'
        print(self.status)
        return super().save(*args, **kwargs)
