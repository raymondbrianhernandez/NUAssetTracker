# Raymond Hernandez
# raymondhernandez@outlook.com
# June 11, 2024
# C:\Users\Owner\assettracker\main\urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('main/', views.main_view, name='main'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('create_account/', views.create_account_view, name='create_account'),
    path('users/', views.users_view, name='users_view'),
]
