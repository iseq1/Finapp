# Generated by Django 5.0.7 on 2024-10-03 16:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0007_income_statistic'),
    ]

    operations = [
        migrations.CreateModel(
            name='Cash_box',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(max_length=255)),
            ],
        ),
    ]
