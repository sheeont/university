from django.db import models
from django.urls import reverse


class Product(models.Model):
    title = models.CharField(max_length=128, verbose_name='Заголовок')
    content = models.TextField(verbose_name='Описание')

    preview = models.ImageField(upload_to=f"images/%Y-%m-%d/", verbose_name='Главное фото', null=True, blank=True)
    on_hover = models.ImageField(upload_to=f"images/%Y-%m-%d/", verbose_name='Фото при наведении', null=True, blank=True)
    additional = models.ImageField(upload_to=f"images/%Y-%m-%d/", verbose_name='Дополнительное фото', null=True, blank=True)

    low_price = models.CharField(max_length=6, default='', verbose_name='Цена за 2,5 мл')
    medium_price = models.CharField(max_length=6, default='', verbose_name='Цена за 5 мл')
    high_price = models.CharField(max_length=6, default='', verbose_name='Цена за 10 мл')

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
