from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    path('#', index, name='about'),  # Сделать якорь к блоку 'О проекте'
    path('catalog/', catalog, name='catalog'),
    path('payment/', payment, name='payment'),
    path('contacts/', contacts, name='contacts'),
]
