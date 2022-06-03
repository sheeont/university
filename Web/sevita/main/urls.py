from django.urls import path
from django.contrib.auth import views

from .views import *

urlpatterns = [
    path('', MainHome.as_view(), name='home'),
    path('catalog/', MainCatalog.as_view(), name='catalog'),
    path('payment/', payment, name='payment'),
    path('product/<slug:prod_slug>/', ShowProduct.as_view(), name='product'),
    path('product/<id>/add', add_to_favorites, name='add'),
    path('product/<id>/remove', remove_from_favorites, name='remove'),
    path('exit/', views.LogoutView.as_view(), name='exit'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
]
