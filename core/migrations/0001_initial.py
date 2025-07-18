# Generated by Django 5.2.4 on 2025-07-12 09:31

import core.models
import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='BalanceGroup',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='BalanceItem',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Account',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(default=core.models.generate_account_number, max_length=10, unique=True)),
                ('name', models.CharField(max_length=255)),
                ('type', models.CharField(choices=[('active', 'Актив'), ('passive', 'Пассив'), ('both', 'Активно-пассивный')], max_length=10)),
                ('balance', models.DecimalField(decimal_places=2, default=0, max_digits=18)),
                ('group', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='accounts', to='core.balancegroup')),
            ],
        ),
        migrations.AddField(
            model_name='balancegroup',
            name='item',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='groups', to='core.balanceitem'),
        ),
    ]
