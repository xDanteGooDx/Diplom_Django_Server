from django.contrib import auth
from django.contrib.auth.models import Group, User
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.views.decorators.csrf import csrf_protect

# Create your views here.
from MySite.forms import RegForm, StudRegForm, ProfileForm, EduRegForm, UploadFileForm
from MySite.models import Test, Question, Answer


def startPage(request):
    return render(request, "MySite/startPage.html", {'args': auth.get_user(request)})


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
    user = auth.get_user(request)
    if user.has_perm('MySite.read_Book'):
        return render(request, "MySite/books.html", {'args': user})
    else:
        return render(request, "MySite/haventAccess.html", {'args': user})


def getTests(request):
    user = auth.get_user(request)
    if user.has_perm('MySite.read_Test'):
        return render(request, "MySite/tests.html", {'args': user})
    else:
        return render(request, "MySite/haventAccess.html", {'args': user})


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
        return HttpResponse("<h1>Тест успешно добавлен</h1>")
    else:
        return render(request, "MySite/addTest.html", {'args': args})


@csrf_protect
def addBook(request):
    args = {}
    args['username'] = auth.get_user(request)
    if request.method == 'POST':
        a = 15
    else:
        form = UploadFileForm()
    return render(request, "MySite/addBook.html", {'args': args, 'form': form})
