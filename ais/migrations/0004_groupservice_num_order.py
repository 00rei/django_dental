# Generated by Django 4.0.5 on 2022-08-26 16:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('ais', '0003_delete_whoviewed'),
    ]

    operations = [
        migrations.AddField(
            model_name='groupservice',
            name='num_order',
            field=models.IntegerField(null=True, verbose_name='Порядковый номер'),
        ),
    ]