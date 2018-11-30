from django.contrib import auth
from django.shortcuts import render, redirect

from django.views.decorators.csrf import csrf_protect


# Create your views here.

def startPage(request):
    return render(request, "MySite/startPage.html", {'username': auth.get_user(request).username})


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
