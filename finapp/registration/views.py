from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import CustomUser, UserProfile

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
            request.session['registration_email'] = email
            request.session['registration_password'] = password
            return redirect('/make-profile')
    return render(request, 'registration.html')


def make_profile(request):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        date_of_birth = request.POST.get('date_of_birth')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')

        email = request.session.get('registration_email')
        password = request.session.get('registration_password')

        if not email or not password:
            return redirect('registration')

        if first_name and last_name and date_of_birth and phone_number and address:
            try:
                # Создание пользователя
                user = CustomUser.objects.create_user(
                    email=email,
                    password=password,
                )

                # Создание профиля пользователя
                UserProfile.objects.create(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    date_of_birth=date_of_birth,
                    phone_number=phone_number,
                    address=address
                )

                # Аутентификация пользователя
                user = authenticate(request, email=email, password=password)
                if user is not None:
                    login(request, user)  # Вход пользователя

                # Очистка данных из сессии
                del request.session['registration_email']
                del request.session['registration_password']

                return redirect('/')  # Перенаправление на домашнюю страницу
            except Exception as e:
                print(f"Error creating user profile: {e}")
                return render(request, 'make-profile.html', {'error': 'Ошибка при создании профиля. Попробуйте снова.'})
    return render(request, 'make-profile.html')


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
