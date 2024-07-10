from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Hello FinAPP.com")


def login(request):
    if request.method == "POST":
        name = request.POST.get("username")
        passw = request.POST.get("pass")
        return HttpResponse(f"<h2>Привет, {name}, твой пароль: {passw}</h2>")
    else:
        return render(request, "login.html")


def registration(request):
    if request.method == "POST":
        name = request.POST.get("username")
        passw = request.POST.get("pass")
        return HttpResponse(f"<h2>Привет, {name}, твой пароль: {passw}</h2>")
    else:
        return render(request, "registration.html")
