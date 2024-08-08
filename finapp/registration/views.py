from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import CustomUser, UserProfile
import re


def is_valid_email(email):
    # Регулярное выражение для проверки формата электронной почты
    email_regex = (r'^[a-zA-Z0-9._%+-]+'
                   r'@'
                   r'[a-zA-Z0-9.-]+'
                   r'\.[a-zA-Z]{2,}$')

    if re.match(email_regex, email):
        return True
    else:
        return False


def is_valid_password(password):
    # Регулярное выражение для проверки условий пароля
    password_regex = (r'^(?=.*[a-z])'
                      r'(?=.*[A-Z])'
                      r'(?=.*\d)'
                      r'(?=.*[!@#$%^&*()_+={}\[\]:;"\'<>,.?/\\|-])'
                      r'.{8,}$')

    if re.match(password_regex, password):
        return True
    else:
        return False


def register_view(request):
    if request.method == 'POST':

        # Получили данные
        email = request.POST['email']
        password = request.POST['password']
        print(email, password)

        # Проверяем данные
        try:
            if is_valid_email(email) and is_valid_password(password):
                request.session['registration_email'] = email
                request.session['registration_password'] = password
                return redirect('/make-profile')
            else:
                print('incorrect!')
        except Exception as e:
            print(e)

    return render(request, 'registration.html')


def make_profile(request):
    if request.method == 'POST':

        # Получили данные
        first_name = request.POST.get('first-name')
        last_name = request.POST.get('last-name')
        date_of_birth = request.POST.get('date-of-birth')
        phone_number = request.POST.get('phone-number')
        address = request.POST.get('address')
        email = request.session.get('registration_email')
        password = request.session.get('registration_password')

        try:
            # Надо проверку данных сделать


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

            return redirect('home')  # Перенаправление на домашнюю страницу
        except Exception as e:
            print(f"Error creating user profile: {e}")
            return render(request, 'make-profile.html', {'error': 'Ошибка при создании профиля. Попробуйте снова.'})

    return render(request, 'make-profile.html')


def sign_up_with_view(request):

    return render(request, 'sign-up-with.html')


def complete_social_registration(request, backend):
    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        date_of_birth = request.POST.get('date_of_birth')
        phone_number = request.POST.get('phone_number')
        address = request.POST.get('address')

        if first_name and last_name and date_of_birth and phone_number and address:
            try:
                social_user = request.user.social_auth.get(provider=backend)
                email = social_user.extra_data['email']

                user, created = CustomUser.objects.get_or_create(email=email)
                if created:
                    user.set_unusable_password()
                    user.save()

                UserProfile.objects.create(
                    user=user,
                    first_name=first_name,
                    last_name=last_name,
                    date_of_birth=date_of_birth,
                    phone_number=phone_number,
                    address=address
                )

                login(request, user)
                return redirect('/')
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
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid email or password'})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')  # Replace 'home' with the name of your homepage URL
