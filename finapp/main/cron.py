from datetime import datetime, date
from django_cron import CronJobBase, Schedule
from .models import Budget, Cash_box, UserProfile, CustomUser


class UpdateBudgetCronJob(CronJobBase):
    # Указываем расписание (ежемесячно)
    RUN_AT_TIMES = ['00:00']
    schedule = Schedule(run_at_times=RUN_AT_TIMES)
    code = 'main.update_budget'  # Уникальный код задачи

    def do(self):

        # Получаем текущую дату
        current_date = date.today()

        # Перебираем всех пользователей в системе
        users = CustomUser.objects.all()

        for user in users:
            # Кэшбоксы обозреваемого пользователя у пользователя
            current_person = UserProfile.objects.get(user=user)
            cash_boxes = current_person.cash_boxes.all()

            # Обновляем последние по дате строки в таблице
            # (Трогаем "Дневные строки" бюджета -> получаем "Месячные строки" бюджета)
            budget_lines = Budget.objects.filter(user=user).order_by('-date')[:len(cash_boxes)]
            for line in budget_lines:
                line.date = current_date
                line.save()

            # Добавляем новые строки в таблицу main_budget для каждого кассового аппарата пользователя
            for cash_box in cash_boxes:
                Budget.objects.create(
                    date=current_date,
                    profit=0,
                    total=Budget.objects.filter(user=user, cash_box=cash_box).order_by('-date')[0].total,
                    cash_box_id=cash_box.id,
                    user_id=user.id
                )


