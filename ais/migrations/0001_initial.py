# Generated by Django 4.0.5 on 2022-06-24 07:59

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fio', models.CharField(max_length=200, verbose_name='ФИО')),
                ('address', models.CharField(max_length=200, verbose_name='Адрес')),
                ('birth_day', models.DateField()),
                ('work_place', models.CharField(max_length=200, verbose_name='Место работы')),
                ('phone', models.CharField(max_length=200, verbose_name='13')),
            ],
        ),
    ]