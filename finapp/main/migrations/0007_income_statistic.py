# Generated by Django 5.0.7 on 2024-09-29 15:11

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0006_expenses_statistic_user'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Income_statistic',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.FloatField()),
                ('percentage', models.FloatField()),
                ('count_of_transactions', models.IntegerField()),
                ('average_transaction', models.FloatField()),
                ('monthly_difference', models.FloatField()),
                ('revenue_growth_rate', models.FloatField()),
                ('category', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='main.category')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
