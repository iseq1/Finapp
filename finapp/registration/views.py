from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import CustomUser

def index(request):
    return HttpResponse("Hello FinAPP.com")


def register_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        # first_name = request.POST.get('first_name')
        # last_name = request.POST.get('last_name')
        # date_of_birth = request.POST.get('date_of_birth')

        if email and password:
            user = CustomUser.objects.create_user(
                email=email,
                password=password,
                # first_name=first_name,
                # last_name=last_name,
                # date_of_birth=date_of_birth
            )
            login(request, user)  # Logs the user in by setting their ID in the session
            return redirect('/')  # Replace 'home' with the name of your homepage URL
    return render(request, 'registration.html')



def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)  # Logs the user in
            return redirect('home')  # Replace 'home' with the name of your homepage URL
        else:
            return render(request, 'registration/login.html', {'error': 'Invalid email or password'})
    return render(request, 'registration/login.html')


def sign_up_with_view(request):

    return render(request, 'sign-up-with.html')



def logout_view(request):
    logout(request)
    return redirect('home')  # Replace 'home' with the name of your homepage URL
