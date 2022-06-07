from django.contrib.auth.decorators import login_required
from django.urls import path
from django.contrib.auth import views

from .views import *

urlpatterns = [
    path('', MainHome.as_view(), name='home'),
    path('catalog/', MainCatalog.as_view(), name='catalog'),
    path('payment/', payment, name='payment'),
    path('product/<slug:prod_slug>/', ShowProduct.as_view(), name='product'),
    path('catalog/add/', login_required(add_to_favorites), name='add'),
    path('catalog/remove/', login_required(remove_from_favorites), name='remove'),
    path('catalog/api/', favorites_api, name='api'),
    path('exit/', views.LogoutView.as_view(), name='exit'),
    path('login/', views.LoginView.as_view(), name='login'),
    path('register/', RegisterUser.as_view(), name='register'),
    path('get_db_changes/', cast_session_to_db, name='get_db_changes')
]
