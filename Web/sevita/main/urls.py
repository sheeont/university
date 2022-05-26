from django.urls import path

from .views import *

urlpatterns = [
    path('', MainHome.as_view(), name='home'),
    path('catalog/', MainCatalog.as_view(), name='catalog'),
    path('payment/', payment, name='payment'),
    path('product/<slug:prod_slug>', show_product, name='product'),
    path('register/', register, name='register')
]
