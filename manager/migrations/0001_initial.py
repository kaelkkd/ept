# Generated by Django 5.0 on 2024-03-06 23:44

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Wallet',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('balance', models.DecimalField(decimal_places=2, max_digits=10)),
                ('monthlySalary', models.DecimalField(decimal_places=2, max_digits=7)),
                ('currencyType', models.CharField(choices=[('USD', 'Dollar'), ('EUR', 'Euro'), ('GBP', 'Pounds'), ('BRL', 'Brazilian real'), ('JPY', 'Japanese yen')], max_length=3)),
                ('owner', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
