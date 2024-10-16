from django.http import HttpResponse, JsonResponse
import json
from django.views.decorators.csrf import csrf_exempt
from django.shortcuts import render, redirect, get_object_or_404
from django.db.models import OuterRef, Subquery, Sum, Count
from .models import CustomUser, UserProfile, Category, Subcategory, Income, Expenses, Expenses_statistic, \
    Income_statistic, Cash_box, Budget
from django.utils import timezone
from calendar import monthrange
from datetime import datetime, date
from .forms import CashBoxForm
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

        # cash_box = Cash_box.objects.create(name='T-Банк')
        # person.cash_boxes.add(cash_box)
        #
        # # Пример получения всех CashBox пользователя:
        # user_cash_boxes = person.cash_boxes.all()
        # print(user_cash_boxes)

        return render(request, 'index.html', context=user_data)
    else:
        return render(request, 'index.html', context={})


def income_page(request):
    categories_income = Category.objects.filter(type="income")
    subcategories = Subcategory.objects.all()
    last_incomes = Income.objects.filter(user=(CustomUser.objects.get(email=request.user)).id).order_by('-date')[:10]

    current_user = (CustomUser.objects.get(email=request.user)).id
    current_person = UserProfile.objects.get(user=current_user)

    income_stat = Income_statistic.objects.filter(user=current_user)
    cash_boxes = current_person.cash_boxes.all()

    data = {
        "categories_income": categories_income,
        "subcategory": subcategories,
        "last_incomes": last_incomes,
        "statistic": income_stat,
        "cash_boxes": cash_boxes,
    }

    if request.method == 'POST':
        try:
            selected_category = request.POST.get('category')
            selected_subcategory = request.POST.get('subcategory')
            selected_total = request.POST.get('total_sum')
            selected_date = request.POST.get('date')
            selected_comment = request.POST.get('comment')
            selected_cashbox = request.POST.get('cashbox')

            if int(selected_category) != 0 and int(selected_subcategory) != 0 and int(
                    selected_cashbox) != 0 and is_valid_price(
                selected_total) and is_valid_date(selected_date):
                Income.objects.create(category=Category.objects.get(id=selected_category),
                                      subcategory=Subcategory.objects.get(id=selected_subcategory),
                                      total=selected_total, date=selected_date, comment=selected_comment,
                                      user=CustomUser.objects.get(email=request.user),
                                      cash_box=Cash_box.objects.get(id=selected_cashbox))

                if timezone.now().month == int(selected_date[5:-3]):
                    budget_update = \
                        Budget.objects.filter(user=current_user, cash_box=Cash_box.objects.get(id=selected_cashbox),
                                              fixed=False)[0]
                else:
                    budget_update = \
                        Budget.objects.filter(user=current_user, cash_box=Cash_box.objects.get(id=selected_cashbox),
                                              fixed=True, date__month=selected_date[5:-3],
                                              date__year=selected_date[:4])[0]
                budget_update.total += float(selected_total)
                budget_update.save()

                for category in categories_income:
                    if Income.objects.filter(user=CustomUser.objects.get(email=request.user),
                                             category=Category.objects.get(id=category.id)):
                        income_statistic, created = Income_statistic.objects.update_or_create(
                            user=CustomUser.objects.get(email=request.user),
                            category=Category.objects.get(id=category.id),
                            defaults={
                                'amount': get_sum(user=current_user,
                                                  category=Category.objects.get(id=category.id),
                                                  type='income'),
                                'percentage': get_percentage(user=current_user,
                                                             category=Category.objects.get(id=category.id),
                                                             type='income'),
                                'count_of_transactions': get_amount_of_transactions(user=current_user,
                                                                                    category=Category.objects.get(
                                                                                        id=category.id),
                                                                                    type='income'),
                                'average_transaction': get_average_transaction(user=current_user,
                                                                               category=Category.objects.get(
                                                                                   id=category.id),
                                                                               type='income'),
                                'revenue_growth_rate': revenue_growth_rate(user=current_user,
                                                                           category=Category.objects.get(
                                                                               id=category.id),
                                                                           type='income'),
                                'monthly_difference': get_monthly_difference(user=current_user,
                                                                             category=Category.objects.get(
                                                                                 id=category.id),
                                                                             type='income'),
                            }
                        )

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


def get_sum(user, category, type):
    # Получаем текущую дату
    today = timezone.now()
    current_month = today.month
    current_year = today.year
    if type == 'expenses':
        # Фильтруем по пользователю, категории и дате
        category_sum = Expenses.objects.filter(
            user=user,
            category=category,
            date__year=current_year,  # Фильтруем по годам
            date__month=current_month  # Фильтруем по месяцам
        ).aggregate(total=Sum('total'))  # Получаем сумму
    elif type == 'income':
        # Фильтруем по пользователю, категории и дате
        category_sum = Income.objects.filter(
            user=user,
            category=category,
            date__year=current_year,  # Фильтруем по годам
            date__month=current_month  # Фильтруем по месяцам
        ).aggregate(total=Sum('total'))  # Получаем сумму
    else:
        raise Exception("Некорректный запрос")
    return category_sum['total'] or 0  # Возвращаем сумму или 0, если нет трат


def get_percentage(user, category, type):
    today = timezone.now()
    current_month = today.month
    current_year = today.year

    if type == 'expenses':
        category_sum = get_sum(user, category, 'expenses')
        total_sum = Expenses.objects.filter(
            user=user,
            date__year=current_year,
            date__month=current_month
        ).aggregate(total=Sum('total'))
    elif type == 'income':
        category_sum = get_sum(user, category, 'income')
        total_sum = Income.objects.filter(
            user=user,
            date__year=current_year,
            date__month=current_month
        ).aggregate(total=Sum('total'))
    else:
        raise Exception("Некорректный запрос")
    return round(float(category_sum) / float(total_sum['total']) * 100, 2) or 0


def get_amount_of_transactions(user, category, type):
    today = timezone.now()
    current_month = today.month
    current_year = today.year
    if type == 'expenses':
        amount_of_transactions = Expenses.objects.filter(
            user=user,
            category=category,
            date__year=current_year,  # Фильтруем по годам
            date__month=current_month  # Фильтруем по месяцам
        ).aggregate(total=Count('total'))
    elif type == 'income':
        amount_of_transactions = Income.objects.filter(
            user=user,
            category=category,
            date__year=current_year,  # Фильтруем по годам
            date__month=current_month  # Фильтруем по месяцам
        ).aggregate(total=Count('total'))
    else:
        raise Exception("Некорректный запрос")

    return amount_of_transactions['total'] or 0


def get_last_transaction(user, category):
    today = timezone.now()
    current_month = today.month
    current_year = today.year

    last_transaction = Expenses.objects.filter(
        user=user,
        category=category,
        date__year=current_year,
        date__month=current_month,
    ).order_by('-date').first()

    return f'{last_transaction.date.strftime('%m/%d/%Y')} \n{last_transaction.comment}' or 'Траты отсутствуют'


def get_max_transaction(user, category):
    today = timezone.now()
    current_month = today.month
    current_year = today.year

    last_transaction = Expenses.objects.filter(
        user=user,
        category=category,
        date__year=current_year,
        date__month=current_month,
    ).order_by('-total').first()

    return f'{last_transaction.date.strftime('%m/%d/%Y')} \n{last_transaction.comment}' or 'Траты отсутствуют'


def get_min_transaction(user, category):
    today = timezone.now()
    current_month = today.month
    current_year = today.year

    last_transaction = Expenses.objects.filter(
        user=user,
        category=category,
        date__year=current_year,
        date__month=current_month,
    ).order_by('-total').last()

    return f'{last_transaction.date.strftime('%m/%d/%Y')} \n{last_transaction.comment}' or 'Траты отсутствуют'


def get_average_transaction(user, category, type):
    now = timezone.now()

    # Получаем год и месяц
    year = now.year
    month = now.month

    # Получаем количество дней в текущем месяце
    days_in_month = monthrange(year, month)[1]
    return round(float(get_sum(user=user, category=category, type=type)) / float(days_in_month), 2) or 0


def get_monthly_difference(user, category, type):
    today = timezone.now()
    current_month = today.month
    current_year = today.year

    # Определяем предыдущий месяц и год
    if current_month == 1:
        previous_month = 12
        previous_year = year - 1
    else:
        previous_month = current_month - 1
        previous_year = current_year

    if type == 'expenses':

        current_sum = Expenses.objects.filter(
            user=user,
            category=category,
            date__year=current_year,
            date__month=current_month
        ).aggregate(total=Sum('total'))

        previous_sum = Expenses.objects.filter(
            user=user,
            category=category,
            date__year=previous_year,
            date__month=previous_month
        ).aggregate(total=Sum('total'))

    elif type == 'income':

        current_sum = Income.objects.filter(
            user=user,
            category=category,
            date__year=current_year,
            date__month=current_month
        ).aggregate(total=Sum('total'))

        previous_sum = Income.objects.filter(
            user=user,
            category=category,
            date__year=previous_year,
            date__month=previous_month
        ).aggregate(total=Sum('total'))

    else:
        raise Exception("Некорректный запрос")
    if current_sum['total'] and previous_sum['total']:
        return current_sum['total'] - previous_sum['total']
    return 0


def revenue_growth_rate(user, category, type):
    today = timezone.now()
    current_month = today.month
    current_year = today.year
    if current_month == 1:
        previous_month = 12
        previous_year = year - 1
    else:
        previous_month = current_month - 1
        previous_year = current_year

    if type == 'expenses':
        previous_sum = Expenses.objects.filter(
            user=user,
            category=category,
            date__year=previous_year,
            date__month=previous_month
        ).aggregate(total=Sum('total'))
    elif type == 'income':
        previous_sum = Income.objects.filter(
            user=user,
            category=category,
            date__year=previous_year,
            date__month=previous_month
        ).aggregate(total=Sum('total'))
    else:
        raise Exception("Некорректный запрос")

    income_difference = get_monthly_difference(user, category, type)

    if previous_sum['total'] and previous_sum['total'] > 0:
        growth_rate = round(float(income_difference) / float(previous_sum['total']), 2) * 100
    else:
        growth_rate = 0

    return growth_rate


def expenses_page(request):
    categories_expenses = Category.objects.filter(type="expenses")
    subcategories = Subcategory.objects.all()
    last_incomes = Expenses.objects.filter(user=(CustomUser.objects.get(email=request.user)).id).order_by('-date')[:10]
    stats = []

    current_user = (CustomUser.objects.get(email=request.user)).id
    current_person = UserProfile.objects.get(user=current_user)

    expenses_stat = Expenses_statistic.objects.filter(user=current_user)
    cash_boxes = current_person.cash_boxes.all()

    data = {
        "category_expenses": categories_expenses,
        "subcategory": subcategories,
        "last_incomes": last_incomes,
        "statistic": expenses_stat,
        "cash_boxes": cash_boxes,
    }

    if request.method == 'POST':
        try:
            selected_category = request.POST.get('category')
            selected_subcategory = request.POST.get('subcategory')
            selected_total = request.POST.get('total_sum')
            selected_date = request.POST.get('date')
            selected_comment = request.POST.get('comment')
            selected_cashbox = request.POST.get('cashbox')

            if int(selected_category) != 0 and int(selected_subcategory) != 0 and is_valid_price(
                    selected_total) and is_valid_date(selected_date):
                Expenses.objects.create(category=Category.objects.get(id=selected_category),
                                        subcategory=Subcategory.objects.get(id=selected_subcategory),
                                        total=selected_total, date=selected_date, comment=selected_comment,
                                        user=CustomUser.objects.get(email=request.user),
                                        cash_box=Cash_box.objects.get(id=selected_cashbox))

                if timezone.now().month == int(selected_date[5:-3]):
                    budget_update = \
                        Budget.objects.filter(user=current_user, cash_box=Cash_box.objects.get(id=selected_cashbox),
                                              fixed=False)[0]
                else:
                    budget_update = \
                        Budget.objects.filter(user=current_user, cash_box=Cash_box.objects.get(id=selected_cashbox),
                                              fixed=True, date__month=selected_date[5:-3],
                                              date__year=selected_date[:4])[0]
                budget_update.total -= float(selected_total)
                budget_update.save()
                for category in categories_expenses:
                    if Expenses.objects.filter(user=CustomUser.objects.get(email=request.user),
                                               category=Category.objects.get(id=category.id)):
                        expenses_statistic, created = Expenses_statistic.objects.update_or_create(
                            user=CustomUser.objects.get(email=request.user),
                            category=Category.objects.get(id=category.id),
                            defaults={
                                'amount': get_sum(user=current_user,
                                                  category=Category.objects.get(id=category.id),
                                                  type='expenses'),
                                'percentage': get_percentage(user=current_user,
                                                             category=Category.objects.get(id=category.id),
                                                             type='expenses'),
                                'count_of_transactions': get_amount_of_transactions(user=current_user,
                                                                                    category=Category.objects.get(
                                                                                        id=category.id),
                                                                                    type='expenses'),
                                'average_transaction': get_average_transaction(user=current_user,
                                                                               category=Category.objects.get(
                                                                                   id=category.id),
                                                                               type='expenses'),
                                'last_transaction': get_last_transaction(user=current_user,
                                                                         category=Category.objects.get(id=category.id)),
                                'max_transaction': get_max_transaction(user=current_user,
                                                                       category=Category.objects.get(id=category.id)),
                                'min_transaction': get_min_transaction(user=current_user,
                                                                       category=Category.objects.get(id=category.id)),
                                'monthly_difference': get_monthly_difference(user=current_user,
                                                                             category=Category.objects.get(
                                                                                 id=category.id),
                                                                             type='expenses'),
                            }
                        )

                return redirect('expenses')
            else:
                raise Exception("Некорректно введены данные для записи!")
        except Exception as e:
            print(f"Ошибка при записи доходов: {e}")
            return render(request, 'expenses_page.html', context=data)

    return render(request, 'expenses_page.html', context=data)


def budget_page(request):
    current_user = (CustomUser.objects.get(email=request.user)).id
    current_person = UserProfile.objects.get(user=current_user)
    try:
        # Для обычного пользователя
        if Budget.objects.filter(user=current_user, fixed=False):

            budget_info_today = Budget.objects.filter(user=current_user, fixed=False)
            # Получаем текущую дату
            current_date = date.today()

            if budget_info_today and any(
                    [line.date for line in budget_info_today]) != current_date and current_date.day != 1:
                for line in budget_info_today:
                    line.date = current_date
                    line.save()

            budget_info = Budget.objects.filter(user=current_user, fixed=True)
            cash_boxes = current_person.cash_boxes.all()
            unique_dates = set(line.date for line in budget_info)
            # Данные о каждом банке в каждую дату
            data = {'fixed_date': {
                str(dates): {
                    cashbox.id: Budget.objects.get(user=current_user, fixed=True, date=dates, cash_box=cashbox).total
                    if Budget.objects.filter(user=current_user, fixed=True, date=dates,
                                             cash_box=cashbox).exists() else '-'
                    for cashbox in cash_boxes
                } for dates in sorted(unique_dates)  # Сортируем даты для порядка
            }}
            # Создаем новый уровень вложенности с ключом "fixed_date"

            # Добавляем 'total_sum' для каждой даты внутри 'fixed_date'
            for dates in unique_dates:
                data['fixed_date'][str(dates)]['total_sum'] = sum(
                    item.total for item in Budget.objects.filter(user=current_user, fixed=True, date=dates)
                )

            # Добавляем 'no_fixed_date'
            data['no_fixed_date'] = {
                str(current_date): {  # Добавляем уровень 'today'
                    cashbox.id: Budget.objects.get(user=current_user, fixed=False, cash_box=cashbox).total
                    if Budget.objects.filter(user=current_user, fixed=False, cash_box=cashbox).exists() else '-'
                    for cashbox in cash_boxes
                }
            }

            # Добавляем 'total_sum' для 'today' внутри 'no_fixed_date'
            data['no_fixed_date'][str(current_date)]['total_sum'] = sum(
                item.total for item in Budget.objects.filter(user=current_user, fixed=False)
            )

            # Добавляем дополнительные данные для HTML-страницы
            data['cashboxes_count'] = len(current_person.cash_boxes.all())
            data['budget_empty'] = False
            data['cashbox_list'] = cash_boxes

            return render(request, 'budget_page.html', context=data)
        else:
            # Для нового пользователя (Проверить, выбрал ли он кэшбоксы, и заполнить бюджет)
            current_date = date.today()
            data = {
                'cashboxes_count': len(current_person.cash_boxes.all()),
                'cashboxes_list': None if len(
                    current_person.cash_boxes.all()) == 0 else current_person.cash_boxes.all(),
                'budget_empty': True,
                'date': current_date,
            }
            if request.method == 'POST':
                try:
                    info = {
                        int(f'{cb.id}'): float(request.POST.get(f'total_for_cashbox_{cb.id}')) for cb in
                        current_person.cash_boxes.all()
                    }
                    print(info)
                    for key, value in info.items():
                        Budget.objects.create(user=CustomUser.objects.get(email=request.user),
                                              cash_box=Cash_box.objects.get(id=key),
                                              date=current_date,
                                              profit=0,
                                              total=value,
                                              fixed=False, )
                        Budget.objects.create(user=CustomUser.objects.get(email=request.user),
                                              cash_box=Cash_box.objects.get(id=key),
                                              date=current_date,
                                              profit=0,
                                              total=value,
                                              fixed=True, )
                    return redirect('budget')
                except Exception as e:
                    print(f"Ошибка при получении данных о новом бюджете: {e}")
                    return render(request, 'budget_page.html', context=data)
            return render(request, 'budget_page.html', context=data)
    except Exception as e:
        print(f"Ошибка при доступе к бюджету: {e}")
        return render(request, 'budget_page.html')


def profile_page(request):
    current_user = (CustomUser.objects.get(email=request.user)).id
    current_person = UserProfile.objects.get(user=current_user)
    cash_boxes = Cash_box.objects.all()
    cash_boxes_user = current_person.cash_boxes.all()

    # create
    if request.method == 'POST':
        form = CashBoxForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('profile')  # Укажите путь на страницу после успешной загрузки
    else:
        form = CashBoxForm()

    # update
    # cashbox = get_object_or_404(Cash_box, pk=3)
    #
    # if request.method == 'POST':
    #     # При POST-запросе обрабатываем форму
    #     form = CashBoxForm(request.POST, request.FILES, instance=cashbox)
    #     if form.is_valid():
    #         form.save()  # Сохраняем изменения
    #         return redirect('profile')  # Переход после успешного редактирования
    # else:
    #     # При GET-запросе отображаем форму с текущими данными объекта
    #     form = CashBoxForm(instance=cashbox)

    data = {
        'person': current_person,
        'user': CustomUser.objects.get(email=request.user),
        'date_joined': str(CustomUser.objects.get(email=request.user).date_joined)[:4],
        'colors': ['purple', 'orange', 'pink', 'green', 'blue', 'yellow'] * math.ceil(len(cash_boxes) / 6),
        'cash_boxes_user': cash_boxes_user,
        'cash_boxes': cash_boxes,
        'color': '#9767ff',
        'form': form
    }
    return render(request, 'profile_page.html', context=data)


@csrf_exempt
def save_selected_cashboxes(request):
    if request.method == 'POST':
        selected_cashboxes = request.POST.get('selected_cashboxes', '')

        if selected_cashboxes:
            # Преобразуем строку в список
            selected_cashboxes = selected_cashboxes.split(',')

            current_user = CustomUser.objects.get(email=request.user.email)
            current_person = UserProfile.objects.get(user=current_user)
            current_date = date.today()

            # Получаем все cash_boxes пользователя
            current_cash_boxes = set(current_person.cash_boxes.values_list('id', flat=True))

            new_user = len(current_cash_boxes) == 0

            # Преобразуем выбранные кассы в set для сравнения
            selected_cashbox_ids = set(map(int, selected_cashboxes))  # Преобразуем в int и set

            # Кассы для добавления (выбранные, но еще не привязанные)
            to_add = selected_cashbox_ids - current_cash_boxes
            # Кассы для удаления (пересечение выбранных и уже привязанных)
            to_remove = current_cash_boxes.intersection(selected_cashbox_ids)
            # Добавление новых связей
            if new_user:
                for cashbox_id in to_add:
                    cashbox = Cash_box.objects.get(id=cashbox_id)
                    current_person.cash_boxes.add(cashbox)
            else:
                for cashbox_id in to_add:
                    cashbox = Cash_box.objects.get(id=cashbox_id)
                    current_person.cash_boxes.add(cashbox)
                    Budget.objects.create(user=current_user,
                                          cash_box=cashbox,
                                          date=current_date,
                                          profit=0,
                                          total=0,
                                          fixed=False, )

            # Удаление ненужных связей
            for cashbox_id in to_remove:
                cashbox = Cash_box.objects.get(id=cashbox_id)
                current_person.cash_boxes.remove(cashbox)
                try:
                    # Тут надо подумать - удалять все записи в бюджете или только нефиксированную
                    # Тут надо подумать - удалять все записи в бюджете или только нефиксированную
                    # Тут надо подумать - удалять все записи в бюджете или только нефиксированную
                    # Тут надо подумать - удалять все записи в бюджете или только нефиксированную
                    Budget.objects.filter(user=current_user, cash_box=cashbox, fixed=False).delete()
                except Exception as e:
                    print(f"Ошибка при удалении бюджета после удаления КБ: {e}")

        return JsonResponse({'success': True})

    return JsonResponse({'success': False})


def update_budget(request):
    current_user = CustomUser.objects.get(email=request.user)
    if request.method == 'POST':
        data = json.loads(request.body)  # Получаем данные
        # Обработка данных
        try:
            for input_id, value in data.items():
                if len(value) != 0 and value != '-':
                    info_line = input_id.split('__')
                    if len(info_line) == 2:
                        date, cashbox_id = info_line[0], info_line[1]
                        budget, created = Budget.objects.update_or_create(
                            date=date,
                            cash_box=Cash_box.objects.get(id=cashbox_id),
                            user=current_user,
                            fixed=True,
                            profit=0,
                            defaults={'total': value}
                        )
                    elif len(info_line) == 3:
                        date, cashbox_id = info_line[0], info_line[1]
                        budget, created = Budget.objects.update_or_create(
                            date=date,
                            cash_box=Cash_box.objects.get(id=cashbox_id),
                            user=current_user,
                            fixed=False,
                            profit=0,
                            defaults={'total': value}
                        )
                elif value == '-':
                    info_line = input_id.split('__')
                    if len(info_line) == 2:
                        date, cashbox_id = info_line[0], info_line[1]
                        budget = Budget.objects.get(date=date, cash_box_id=Cash_box.objects.get(id=cashbox_id),
                                                    user=current_user, fixed=True)
                        budget.delete()

                    elif len(info_line) == 3:
                        date, cashbox_id = info_line[0], info_line[1]
                        budget = Budget.objects.get(date=date, cash_box_id=Cash_box.objects.get(id=cashbox_id),
                                                    user=current_user, fixed=False)
                        budget.delete()

        except Exception as e:
            print(f"Ошибка при обновлении бюджета: {e}")

        return JsonResponse({"status": "success", "message": "Данные успешно обновлены."})

    return JsonResponse({"status": "error", "message": "Неверный метод запроса."})
