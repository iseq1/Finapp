from django.http import HttpResponse, JsonResponse
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.db.models import OuterRef, Subquery, Sum, Count
from .models import CustomUser, UserProfile, Category, Subcategory, Income, Expenses
from django.utils import timezone
from calendar import monthrange
from datetime import datetime
import math
import re


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
    categories_income = Category.objects.filter(type="income")
    subcategories = Subcategory.objects.all()
    last_incomes = Income.objects.filter(user=(CustomUser.objects.get(email=request.user)).id).order_by('-date')[:10]
    data = {
        "category_income": categories_income,
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


def get_subcategories(request):
    category_id = request.GET.get('category_id')
    if category_id:
        subcategories = Subcategory.objects.filter(category_id=category_id).values('id', 'name')
        return JsonResponse(list(subcategories), safe=False)
    return JsonResponse([], safe=False)


def get_expenses_sum(user, category):
    # Получаем текущую дату
    today = timezone.now()
    current_month = today.month
    current_year = today.year

    # Фильтруем по пользователю, категории и дате
    expenses_sum = Expenses.objects.filter(
        user=user,
        category=category,
        date__year=current_year,   # Фильтруем по годам
        date__month=current_month   # Фильтруем по месяцам
    ).aggregate(total=Sum('total'))  # Получаем сумму
    return expenses_sum['total'] or 0  # Возвращаем сумму или 0, если нет трат


def get_percentage(user, category):
    today = timezone.now()
    current_month = today.month
    current_year = today.year

    category_sum = get_expenses_sum(user, category)
    total_sum = Expenses.objects.filter(
        user=user,
        date__year=current_year,
        date__month=current_month
    ).aggregate(total=Sum('total'))
    return f"{round(float(category_sum)/float(total_sum['total']) * 100, 2)} %"  or 0


def get_amount_of_transactions(user, category):
    today = timezone.now()
    current_month = today.month
    current_year = today.year

    amount_of_transactions = Expenses.objects.filter(
        user=user,
        category=category,
        date__year=current_year,  # Фильтруем по годам
        date__month=current_month  # Фильтруем по месяцам
    ).aggregate(total=Count('total'))

    return amount_of_transactions['total'] or 0


def get_last_transaction(user, category):
    today = timezone.now()
    current_month = today.month
    current_year = today.year

    last_transaction = Expenses.objects.filter(
        user = user,
        category = category,
        date__year = current_year,
        date__month = current_month,
    ).order_by('-date').first()

    return f'{last_transaction.date.strftime('%m/%d/%Y')} \n{last_transaction.comment}' or 'Траты отсутствуют'


def get_max_transaction(user, category):
    today = timezone.now()
    current_month = today.month
    current_year = today.year

    last_transaction = Expenses.objects.filter(
        user = user,
        category = category,
        date__year = current_year,
        date__month = current_month,
    ).order_by('-total').first()

    return f'{last_transaction.date.strftime('%m/%d/%Y')} \n{last_transaction.comment}' or 'Траты отсутствуют'


def get_min_transaction(user, category):
    today = timezone.now()
    current_month = today.month
    current_year = today.year

    last_transaction = Expenses.objects.filter(
        user = user,
        category = category,
        date__year = current_year,
        date__month = current_month,
    ).order_by('-total').last()

    return f'{last_transaction.date.strftime('%m/%d/%Y')} \n{last_transaction.comment}' or 'Траты отсутствуют'


def get_average_transaction(user, category):
    now = timezone.now()

    # Получаем год и месяц
    year = now.year
    month = now.month

    # Получаем количество дней в текущем месяце
    days_in_month = monthrange(year, month)[1]
    return f'{round(float(get_expenses_sum(user=user, category=category))/float(days_in_month),2)}' or 'Траты отсутствуют'


def expenses_page(request):

    categories_expenses = Category.objects.filter(type="expenses")
    subcategories = Subcategory.objects.all()
    last_incomes = Expenses.objects.filter(user=(CustomUser.objects.get(email=request.user)).id).order_by('-date')[:10]
    stats = []

    current_user = (CustomUser.objects.get(email=request.user)).id
    for category in categories_expenses:
        stats.append(
            [
                category.name,
                get_expenses_sum(user=current_user, category=Category.objects.get(id=category.id)),
                get_percentage(user=current_user, category=Category.objects.get(id=category.id)),
                get_amount_of_transactions(user=current_user, category=Category.objects.get(id=category.id)),
                get_average_transaction(user=current_user, category=Category.objects.get(id=category.id)),
                get_last_transaction(user=current_user, category=Category.objects.get(id=category.id)),
                get_max_transaction(user=current_user, category=Category.objects.get(id=category.id)),
                get_min_transaction(user=current_user, category=Category.objects.get(id=category.id)),
            ]
        )

    data = {
        "category_expenses": categories_expenses,
        "subcategory": subcategories,
        "last_incomes": last_incomes,
        "statistic": stats
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
