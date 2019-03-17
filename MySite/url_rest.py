from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('answer', views.AnswerView)
router.register('book', views.BookView)
router.register('text', views.TextView)
router.register('test', views.TestView)
router.register('user', views.UserView)
router.register('fulltext', views.FullTextView)

urlpatterns = [
    path('login', views.api_login, name='rest_login'),
    path('getfulltext/<num>', views.getFullText, name='getFullText'),
    path('getheader/<num>', views.getHeader, name='getHeader'),
    path('gettext/<num>', views.getText, name='getText'),
    path('', include(router.urls)),
]
