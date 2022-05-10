from django.db import models
from django.urls import reverse


class Product(models.Model):
    title = models.CharField(max_length=128, verbose_name='Заголовок')
    price = models.CharField(max_length=64, default='', verbose_name='Цена')
    content = models.TextField(verbose_name='Описание')
    photo = models.ImageField(upload_to=f"images/%Y-%m-%d/", verbose_name='Фото')
    time_create = models.DateTimeField(auto_now_add=True, verbose_name='Время создания')
    time_update = models.DateTimeField(auto_now=True, verbose_name='Время обновления')
    is_visible = models.BooleanField(default=True, verbose_name='Видимость')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse('catalog', kwargs={'prod_id': self.pk})

    class Meta:
        verbose_name = 'Товар'
        verbose_name_plural = 'Каталог'
        ordering = ['-time_create', 'title']
