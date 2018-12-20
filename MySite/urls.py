from django.urls import path, include
from . import views
from rest_framework import routers

router = routers.DefaultRouter()
router.register('answer', views.AnswerView)
router.register('book', views.BookView)
router.register('text', views.TextView)

urlpatterns = [
    path('', views.startPage, name='startPage'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name='logout'),
    path('student_registration/', views.studReg, name='studReg'),
    path('educator_registration/', views.eduReg, name='eduReg'),
    path('books/', views.getBooks, name='getBooks'),
    path('books/addbook', views.addBook, name='addBook'),
    path('tests/', views.getTests, name='getTests'),
    path('tests/addtest', views.addTest, name='addTest'),
    path('tests/<number>/', views.makeTest, name='makeTest'),
    path('books/<number>/', views.readBook, name='readBook'),
    path('help/', views.getHelp, name='getHelp'),
    path('about/', views.getAbout, name='getAbout'),
    path('rest/', include(router.urls)),
    path('backup/', views.backup, name='backup'),
    path('dobackup/', views.doBackup, name='doBackup'),
]
