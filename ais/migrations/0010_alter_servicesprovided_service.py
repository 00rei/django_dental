# Generated by Django 4.0.5 on 2022-09-02 08:42

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('ais', '0009_photo_date_create'),
    ]

    operations = [
        migrations.AlterField(
            model_name='servicesprovided',
            name='service',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='ais.service', verbose_name='Код услуги'),
        ),
    ]
