from django.urls import path

from .views import *

urlpatterns = [
    path('', index, name='home'),
    # path('', index, name='about'),
    path('catalog/', catalog, name='catalog'),
    path('payment/', payment, name='payment'),
    path('contacts/', contacts, name='contacts'),
    path('product/<int:prod_id>', show_product, name='product')
]
