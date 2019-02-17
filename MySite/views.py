import base64
import os
import socket
import string
import subprocess
import time

from django.core import serializers
from django.contrib import auth
from django.contrib.auth.models import Group, User
from django.http import HttpResponse
from django.shortcuts import render, redirect
from rest_framework import viewsets
from django.core.mail import send_mail
from django.views.decorators.csrf import csrf_protect
from django.db import connection

# Create your views here.
from Diplom import settings
from MySite.forms import RegForm, StudRegForm, ProfileForm, EduRegForm, UploadFileForm, BookForm
from MySite.models import Test, Question, Answer, TestResult, Book, Text, FullText, Header
from .serializers import AnswerSerializers, BookSerializers, TextSerializers, TestSerializers


def startPage(request):
    args = {}
    args['username'] = auth.get_user(request)
    return render(request, "MySite/startPage.html", {'args': args})


@csrf_protect
def login(request):
    args = {}
    if request.POST:
        username = request.POST.get('username', '')
        password = request.POST.get('password', '')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            return redirect("/")
        else:
            args['login_error'] = "Пользователь не найден"
            return render(request, "MySite/signinPage.html", args)
    else:
        return render(request, "MySite/signinPage.html", args)


def logout(request):
    auth.logout(request)
    return redirect("/")


@csrf_protect
def studReg(request):
    args = {}
    regForm = RegForm
    studForm = StudRegForm
    profile = ProfileForm
    if request.method == 'POST':
        form = RegForm(request.POST)
        studForm = StudRegForm(request.POST)
        profile = ProfileForm(request.POST)
        if form.is_valid() and studForm.is_valid() and profile.is_valid():
            user = form.save()
            # user.is_active = False
            # user.save()
            user.profile.patronymic = request.POST.get('patronymic')
            user.profile.birth = '{0}-{1}-{2}'.format(request.POST.get('birth_year'), request.POST.get('birth_month'),
                                                      request.POST.get('birth_day'))
            user.profile.save()
            my_group = Group.objects.get(name='Students')
            my_group.user_set.add(user)
            student = studForm.save(commit=False)
            student.profile_id = user.profile.id
            studForm.save()
            return render(request, "MySite/successfulRegistration.html", {'user': user})
        else:
            args['errors_form'] = form.errors
            args['errors_stud'] = studForm.errors
            args['errors_profile'] = profile.errors
            return render(request, "MySite/studentRegistration.html",
                          {'regForm': regForm, 'studForm': studForm, 'args': args, 'profile': profile})
    else:
        return render(request, "MySite/studentRegistration.html",
                      {'regForm': regForm, 'studForm': studForm, 'args': args, 'profile': profile})


def getBooks(request):
    args = {}
    user = auth.get_user(request)
    args['username'] = user
    if user.has_perm('MySite.read_Book'):
        args['books'] = Book.objects.all().order_by("-id")
        return render(request, "MySite/books.html", {'args': args})
    else:
        return render(request, "MySite/haventAccess.html", {'args': args})


def getTests(request):
    args = {}
    user = auth.get_user(request)
    args['username'] = user
    if user.has_perm('MySite.read_Test'):
        args['tests'] = Test.objects.all().order_by("-id")
        return render(request, "MySite/tests.html", {'args': args})
    else:
        return render(request, "MySite/haventAccess.html", {'args': args})


@csrf_protect
def eduReg(request):
    args = {}
    regForm = RegForm
    profile = ProfileForm
    if request.method == 'POST':
        form = RegForm(request.POST)
        profile = ProfileForm(request.POST)
        eduForm = EduRegForm(request.POST)
        if form.is_valid() and profile.is_valid():
            user = form.save()
            # user.is_active = False
            # user.save()
            user.profile.patronymic = request.POST.get('patronymic')
            user.profile.birth = '{0}-{1}-{2}'.format(request.POST.get('birth_year'), request.POST.get('birth_month'),
                                                      request.POST.get('birth_day'))
            user.profile.save()
            my_group = Group.objects.get(name='Educators')
            my_group.user_set.add(user)
            educator = eduForm.save(commit=False)
            educator.profile_id = user.profile.id
            educator.save()
            return render(request, "MySite/successfulRegistration.html", {'user': user})
        else:
            args['errors_form'] = form.errors
            args['errors_profile'] = profile.errors
            return render(request, "MySite/educatorRegistration.html",
                          {'regForm': regForm, 'args': args, 'profile': profile})
    else:
        return render(request, "MySite/educatorRegistration.html",
                      {'regForm': regForm, 'args': args, 'profile': profile})


@csrf_protect
def addTest(request):
    args = {}
    args['username'] = auth.get_user(request)
    if request.method == 'POST':
        newTest = Test()
        newTest.test_title = request.POST.get('name_test')
        newTest.about = request.POST.get('about_test')
        newTest.author = auth.get_user(request)
        newTest.save()
        num = 1
        while num is not None:
            newQuestion = Question()
            search = request.POST.get('question_' + str(num))
            if search is not None:
                newQuestion.question_text = search
                newQuestion.get_score = 1
                newQuestion.id_test = newTest
                newQuestion.save()
                num2 = 1
                while num2 is not None:
                    newAnswer = Answer()
                    search = request.POST.get('answer_' + str(num) + '_' + str(num2))
                    if search is not None:
                        newAnswer.answer_text = search
                        newAnswer.id_question = newQuestion
                        search = request.POST.get('checkbox_' + str(num) + '_' + str(num2))
                        if search is not None:
                            newAnswer.is_right = True
                        else:
                            newAnswer.is_right = False
                        newAnswer.save()
                    else:
                        num2 = None
                    if num2 is not None:
                        num2 += 1
            else:
                num = None
            if num is not None:
                num += 1
        return render(request, "MySite/successfulAddTest.html", {'args': args})
    else:
        return render(request, "MySite/addTest.html", {'args': args})


@csrf_protect
def addBook(request):
    args = {}
    args['username'] = auth.get_user(request)
    if request.method == 'POST':
        form = UploadFileForm(request.POST, request.FILES)
        book = BookForm(request.POST, request.FILES)
        if book.is_valid() and form.is_valid():
            book_model = Book()
            book_model.author = auth.get_user(request)
            book_model.title_book = book['title_book'].value()
            if not ('icon_book' in request.FILES):
                book_model.icon_book = 'uploads/default_icon.jpeg'
            else:
                book_model.icon_book = book['icon_book'].value()
            book_model.save()
            # =====
            text_model = FullText()
            text_model.text_html = form['text_html'].value()
            text_model.id_book = book_model
            text_model.save()
            # ======
            path_to_html = settings.MEDIA_ROOT + '/' + os.path.splitext(text_model.text_html.name)[0] + '.files'
            os.makedirs(path_to_html)
            for item in request.FILES.getlist('text_source'):
                with open(path_to_html + '/' + item.name, "wb+") as destination:
                    for chuck in item.chunks():
                        destination.write(chuck)

            head_text = ""
            path = settings.MEDIA_ROOT + '/' + text_model.text_html.name
            file = open(path, "r")
            src = 'src="'
            while True:
                line = file.readline()
                head_text += line
                if not line or (line.find('<body') >= 0):
                    break
            header_flag = False
            name_header = 1
            text_header = ''
            text_header_flag = False
            new_header = None
            while True:
                line = file.readline()
                if line.find('<h1>') >= 0:
                    text_header_flag = True
                    if header_flag == False:
                        new_header = open(
                            settings.MEDIA_ROOT + '/' + os.path.splitext(text_model.text_html.name)[0] + '_' + str(
                                name_header) + '.html',
                            'w')
                        new_header.write(head_text)
                        header_flag = True
                    else:
                        new_header.write('</body>\n')
                        new_header.write('</html>')
                        new_header.close()
                        new_header_model = Header()
                        new_header_model.id_book = book_model
                        new_header_model.text_header = text_header.replace('<h1>', '').replace('\n', '').replace('\t',
                                                                                                                 '')
                        new_header_model.save()
                        text_header = ''
                        new_text = Text()
                        new_text.id_header = new_header_model
                        new_text.text_html = settings.MEDIA_ROOT + '/' + os.path.splitext(text_model.text_html.name)[
                            0] + '_' + str(
                            name_header) + '.html'
                        new_text.save()
                        name_header += 1
                        new_header = open(
                            settings.MEDIA_ROOT + '/' + os.path.splitext(text_model.text_html.name)[0] + '_' + str(
                                name_header) + '.html',
                            'w')
                        new_header.write(head_text + line)
                if line.find('</h1>') >= 0:
                    text_header_flag = False
                if header_flag:
                    new_header.write(line)
                    if text_header_flag:
                        text_header += line
                if not line and header_flag:
                    new_header.close()
                    new_header_model = Header()
                    new_header_model.id_book = book_model
                    new_header_model.text_header = text_header.replace('<h1>', '').replace('\n', '').replace('\t',
                                                                                                             '')
                    new_header_model.save()
                    text_header = ''
                    new_text = Text()
                    new_text.id_header = new_header_model
                    new_text.text_html = settings.MEDIA_ROOT + '/' + os.path.splitext(text_model.text_html.name)[
                        0] + '_' + str(
                        name_header) + '.html'
                    new_text.save()
                    break
                if not line:
                    break
            return render(request, "MySite/successfulAddBook.html", {'args': args})
    else:
        form = UploadFileForm()
        book = BookForm()
        return render(request, "MySite/addBook.html", {'args': args, 'form': form, 'book': book})


def editor(request):
    args = {}
    args['username'] = auth.get_user(request)
    if request.method == 'POST':
        book = BookForm(request.POST, request.FILES)
        if book.is_valid():
            book_model = Book()
            book_model.author = auth.get_user(request)
            book_model.title_book = book['title_book'].value()
            if not ('icon_book' in request.FILES):
                book_model.icon_book = 'uploads/default_icon.jpeg'
            else:
                book_model.icon_book = book['icon_book'].value()
            book_model.save()
            return render(request, "MySite/successfulAddBook.html", {'args': args})
    else:
        book = BookForm()
        return render(request, "MySite/editor.html", {'args': args, 'book': book})


@csrf_protect
def makeTest(request, number):
    all_score = 0
    score = 0
    args = {}
    args['username'] = auth.get_user(request)
    args['Test'] = Test.objects.get(id=number)
    args['Question'] = Question.objects.filter(id_test=number)
    args['Answer'] = Answer.objects.all()
    if request.method == 'POST':
        for item in args['Question']:
            for item2 in args['Answer'].filter(id_question=item.id):
                if item2.is_right:
                    if request.POST.get('checkbox_' + str(item.id) + '_' + str(item2.id)):
                        score += 1
            all_score += 1
        args['all_score'] = all_score
        args['score'] = score
        new_result = TestResult()
        new_result.id_test = args['Test']
        new_result.id_student = auth.get_user(request)
        new_result.score = score
        value = TestResult.objects.filter(id_test=args['Test'], id_student=auth.get_user(request)).order_by(
            '-attempts').first()
        if value is not None:
            new_result.attempts = value.attempts + 1
        else:
            new_result.attempts = 1
        new_result.save()
        return render(request, "MySite/getScore.html", {'args': args})
    else:
        return render(request, "MySite/makeTest.html", {'args': args})


def readBook(request, number):
    args = {}
    args['username'] = auth.get_user(request)
    args['book'] = Book.objects.get(id=number)
    args['content'] = FullText.objects.get(id_book=number)
    return render(request, "MySite/readBook.html", {'args': args})


def getHelp(request):
    args = {}
    args['username'] = auth.get_user(request)
    return render(request, "MySite/help.html", {'args': args})


def getAbout(request):
    args = {}
    args['username'] = auth.get_user(request)
    # send_mail(
    #     'Subject here',
    #     'Here is the message.',
    #     settings.EMAIL_HOST_USER,
    #     ['konyukov1997@inbox.ru'],
    #     fail_silently=False,
    # )
    # SMTP_send_message('konyukov1997@gmail.com', 'dantegood',
    #                   ['konyukov1997@inbox.ru', 'konyukov1997@icloud.com'], 'test',
    #                   str(auth.get_user(request).username) + + str(auth.get_user(request).password))
    return render(request, "MySite/about.html", {'args': args})


def backup(request):
    cursor = connection.cursor()
    cursor.execute("USE master exec backup_db")

    return HttpResponse("<h1> Вы сделали резервную копию</h1")


def restore(request):
    cursor = connection.cursor()
    cursor.execute("USE master exec restore_db")
    return HttpResponse("<h1> Вы восстановили из резервной копии</h1")


class AnswerView(viewsets.ModelViewSet):
    queryset = Answer.objects.all()
    serializer_class = AnswerSerializers


class BookView(viewsets.ModelViewSet):
    queryset = Book.objects.all()
    serializer_class = BookSerializers


class TextView(viewsets.ModelViewSet):
    queryset = Text.objects.all()
    serializer_class = TextSerializers


class TestView(viewsets.ModelViewSet):
    queryset = Test.objects.all()
    serializer_class = TestSerializers
