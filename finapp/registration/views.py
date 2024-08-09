from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate, logout
from .models import CustomUser, UserProfile
import re


def is_valid_email(email, type='registration'):
    # Регулярное выражение для проверки формата электронной почты
    email_regex = (r'^[a-zA-Z0-9._%+-]+'
                   r'@'
                   r'[a-zA-Z0-9.-]+'
                   r'\.[a-zA-Z]{2,}$')
    if type == 'registration':
        try:
            # Если уже есть пользователь с таким email -> False
            existing_user = CustomUser.objects.get(email=email)
            return False
        except Exception as e:
            if re.match(email_regex, email):
                return True
            else:
                return False

    elif type == 'login':
        try:
            # Если уже есть пользователь с таким email -> True
            existing_user = CustomUser.objects.get(email=email)
            if re.match(email_regex, email):
                return True
            else:
                return False
        except Exception as e:
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
        print(is_valid_email(email), is_valid_email('egorka.mironov.2003@mail.ru'))

        # Проверяем данные
        try:
            if is_valid_email(email) and is_valid_password(password):
                request.session['registration_email'] = email
                request.session['registration_password'] = password
                return redirect('/make-profile')
            else:
                raise Exception("Некорректный ввод данных")
        except Exception as e:
            print(f"Ошибка при создании профиля: {e}")
            return render(request, 'registration.html', {'error': f'Ошибка при создании профиля - {e}. Попробуйте снова.'})

    return render(request, 'registration.html')


def is_valid_name(name):
    name_regex = r"^[A-Za-zА-Яа-яЁё\s-]+$"
    if re.match(name_regex, name) and 1 <= len(name) <= 30:
        return True
    else:
        return False


def is_leap_year(year):
    return (year % 4 == 0 and year % 100 != 0) or (year % 400 == 0)


def days_in_month(month, year):
    if month in [1, 3, 5, 7, 8, 10, 12]:
        return 31
    elif month in [4, 6, 9, 11]:
        return 30
    elif month == 2:
        return 29 if is_leap_year(year) else 28


def is_valid_date_of_birth(date_of_birth):
    date_regex = r"^\d{4}-(0[1-9]|1[0-2])-(0[1-9]|[12][0-9]|3[01])$"
    match = re.match(date_regex, date_of_birth)
    if match:
        year, month, day = map(int, date_of_birth.split('-'))
        if day <= days_in_month(month, year):
            return True
    return False


def is_valid_phone_number(phone_number):
    # Проверяем, что строка состоит только из цифр и имеет длину 11
    if len(phone_number) == 11 and phone_number.isdigit() and (phone_number.startswith('8') or phone_number.startswith('7')):
        return True
    return False


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
            if is_valid_name(first_name) and is_valid_name(last_name) and is_valid_date_of_birth(date_of_birth) and is_valid_phone_number(phone_number) and address:

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
            else:
                raise Exception("Некорректный ввод данных")
        except Exception as e:
            print(f"Ошибка при создании профиля: {e}")
            return render(request, 'make-profile.html', {'error': f'Ошибка при создании профиля - {e}. Попробуйте снова.'})

    return render(request, 'make-profile.html')


def login_view(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']
        try:
            if is_valid_email(email, type='login') and is_valid_password(password):
                # Аутентификация пользователя с использованием email и пароля
                user = authenticate(request, username=email, password=password)
                if user is not None:
                    # Если пользователь найден, выполняем логин
                    login(request, user)
                    return redirect('home')  # Перенаправление на главную страницу или другую
                else:
                    raise Exception("Неправильный email или пароль")
            else:
                raise Exception("Некорректный email или пароль")
        except Exception as e:
            return render(request, 'login.html', {'error': f'Ошибка при авторизации - {e}. Попробуйте снова.'})
    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('home')  # Replace 'home' with the name of your homepage URL
