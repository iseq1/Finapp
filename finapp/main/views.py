from django.http import HttpResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from .models import CustomUser, UserProfile, Category, Subcategory, Income, Expenses
import re
from datetime import datetime


def is_valid_date(date_str, date_format="%Y-%m-%d"):
    try:
        # Попробуем преобразовать строку в дату по указанному формату
        datetime.strptime(date_str, date_format)
        return True
    except ValueError:
        return False


def is_valid_price(price_str):
    # Регулярное выражение для проверки формата числа с точкой или запятой
    pattern = r'^\d+([.,]\d{1,2})?$'
    if re.match(pattern, price_str):
        return True
    return False


# Create your views here.
def index(request):
    if request.user.is_authenticated:
        user_id = request.user.email
        user = CustomUser.objects.get(email=user_id)
        person = UserProfile.objects.get(user=user)
        user_data = {
            "name": person.first_name,
            "surname": person.last_name,
            "address": person.address,
            "tel": person.phone_number,
            "db": person.date_of_birth,
        }
        return render(request, 'index.html', context=user_data)
    else:
        return render(request, 'index.html', context={})


def income_page(request):
    categories = Category.objects.all()
    categories_income = Category.objects.filter(type="income")
    subcategories = Subcategory.objects.all()
    last_incomes = Income.objects.filter(user=(CustomUser.objects.get(email=request.user)).id).order_by('-date')[:10]
    data = {
        "category": categories,
        "category_income": categories_income,
        "category_expenses": categories_expenses,
        "subcategory": subcategories,
        "last_incomes": last_incomes
    }
    if request.method == 'POST':
        try:
            selected_category = request.POST.get('category')
            selected_subcategory = request.POST.get('subcategory')
            selected_total = request.POST.get('total_sum')
            selected_date = request.POST.get('date')
            selected_comment = request.POST.get('comment')
            if int(selected_category) != 0 and int(selected_subcategory) != 0 and is_valid_price(selected_total) and is_valid_date(selected_date):
                # Income.objects.create(category=Category.objects.get(id=selected_category),
                #                       subcategory=Subcategory.objects.get(id=selected_subcategory),
                #                       total=selected_total, date=selected_date, comment=selected_comment,
                #                       user=CustomUser.objects.get(email=request.user))

                return redirect('income')
            else:
                raise Exception("Некорректно введены данные для записи!")
        except Exception as e:
            print(f"Ошибка при записи доходов: {e}")
            return render(request, 'income_page.html', context=data)

    return render(request, 'income_page.html', context=data)



def expenses_page(request):
    categories = Category.objects.all()
    subcategories = Subcategory.objects.all()
    categories_expenses = Category.objects.filter(type="expenses")
    last_incomes = Expenses.objects.filter(user=(CustomUser.objects.get(email=request.user)).id).order_by('-date')[:10]

    data = {
        "category": categories,
        "category_expenses": categories_expenses,
        "subcategory": subcategories,
        "last_incomes": last_incomes
    }
    if request.method == 'POST':
        try:
            selected_category = request.POST.get('category')
            selected_subcategory = request.POST.get('subcategory')
            selected_total = request.POST.get('total_sum')
            selected_date = request.POST.get('date')
            selected_comment = request.POST.get('comment')
            if int(selected_category) != 0 and int(selected_subcategory) != 0 and is_valid_price(selected_total) and is_valid_date(selected_date):
                Expenses.objects.create(category=Category.objects.get(id=selected_category),
                                      subcategory=Subcategory.objects.get(id=selected_subcategory),
                                      total=selected_total, date=selected_date, comment=selected_comment,
                                      user=CustomUser.objects.get(email=request.user))

                return redirect('expenses')
            else:
                raise Exception("Некорректно введены данные для записи!")
        except Exception as e:
            print(f"Ошибка при записи доходов: {e}")
            return render(request, 'expenses_page.html', context=data)

    return render(request, 'expenses_page.html', context=data)
