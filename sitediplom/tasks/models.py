from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils.text import slugify
from unidecode import unidecode


class Tasks(models.Model):
    CHOICES_PRIORITY = {
        1: 'Низкий',
        2: 'Ниже среднего',
        3: 'Средний',
        4: 'Выше среднего',
        5: 'Высокий'
    }
    title = models.CharField(max_length=100, verbose_name='Загаловок')
    description = models.TextField(blank=True, verbose_name='Описание')
    completed = models.BooleanField(default=False, verbose_name='Завершена')
    is_favorite = models.BooleanField(default=False, verbose_name='Избранная')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    completed_at = models.DateField(verbose_name='Дата завершения', null=True, blank=True)
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE, default=1)
    priority = models.IntegerField(choices=CHOICES_PRIORITY, verbose_name='Приорететность', null=True)
    slug = models.SlugField(max_length=150, unique=True, db_index=True, verbose_name='URL', null=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            ascii_title = unidecode(self.title)
            self.slug = slugify(ascii_title)
        super().save(*args, **kwargs)

    def get_absolute_url(self):
        return reverse('view_task', kwargs={'task_slug': self.slug})


    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'задача'
        verbose_name_plural = 'Задачи'
        ordering = ['id', 'priority']


class FavoriteTask(models.Model):
    favorites = models.ForeignKey(Tasks, on_delete=models.CASCADE, verbose_name='Избранная задача',
                                  related_name='all_favorites')
    user = models.ForeignKey(User, verbose_name='Пользователь', on_delete=models.CASCADE)
    slug = models.SlugField(max_length=150, unique=True, db_index=True, verbose_name='URL', null=True)
    is_favorite = models.BooleanField(default=False, verbose_name='Избранная')

    def __str__(self):
        return f'{self.favorites.title} - {self.user.username}'

    class Meta:
        verbose_name = 'избранная'
        verbose_name_plural = 'Избранные'

    def get_absolute_url(self):
        return reverse('favorites', kwargs={'favorites_slug': self.slug})
    