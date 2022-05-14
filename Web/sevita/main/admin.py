from django.contrib import admin

from .models import *


class ProductAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'time_create', 'preview', 'is_visible')
    list_display_links = ('id', 'title')
    search_fields = ('title', 'content')
    list_editable = ('is_visible',)
    prepopulated_fields = {'slug': ("title",)}


admin.site.register(Product, ProductAdmin)
