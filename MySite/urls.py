from django.urls import path
from . import views

urlpatterns = [
    path('', views.startPage, name='startPage'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
]
