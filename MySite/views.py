from django.contrib import auth
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.template.context_processors import csrf

from django.views.decorators.csrf import csrf_protect

# Create your views here.
from MySite.forms import RegForm, StudRegForm


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
    if request.method == 'POST':
        form = RegForm(request.POST)
        studForm = StudRegForm(request.POST)
        if form.is_valid():
            if studForm.is_valid():
                user = form.save(commit=False)
                user.profile.patronymic = form.cleaned_data.get('patronymic')
                user.is_active = False
                user.save()
                student = studForm.save(commit=False)
                student.profile_id = user.profile.id
                studForm.save()
                return HttpResponse("<h1>student</h1>")
            else:
                args['errors'] = form.errors + studForm.errors
        else:
            args['errors'] = form.errors

            return render(request, "MySite/studentRegistration.html", {'regForm': regForm,
                                                                       'studForm': studForm, 'args': args})
    else:
        return render(request, "MySite/studentRegistration.html",
                      {'regForm': regForm, 'studForm': studForm, 'args': args})
