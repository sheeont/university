from django.db import models


class Product(models.Model):
    title = models.CharField(max_length=128)
    price = models.CharField(max_length=64, default='')
    content = models.TextField()
    photo = models.ImageField(upload_to=f"images/{title}/")
    time_create = models.DateTimeField(auto_now_add=True)
    time_update = models.DateTimeField(auto_now=True)
    is_visible = models.BooleanField(default=True)

    def __str__(self):
        return self.title
