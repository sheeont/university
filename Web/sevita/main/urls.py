from django.urls import path
from django.contrib.auth import views

from .views import *

urlpatterns = [
    path('', MainHome.as_view(), name='home'),
    path('catalog/', MainCatalog.as_view(), name='catalog'),
    path('payment/', payment, name='payment'),
    path('product/<slug:prod_slug>', ShowProduct.as_view(), name='product'),
    path('exit/', views.LogoutView.as_view(), name='exit'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
]
