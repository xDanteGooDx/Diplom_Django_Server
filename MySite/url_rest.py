from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('answer', views.AnswerView)
router.register('book', views.BookView)
router.register('text', views.TextView)
router.register('test', views.TestView)

urlpatterns = [
    path('login', views.api_login, name='rest_login'),
    path('', include(router.urls))
]
