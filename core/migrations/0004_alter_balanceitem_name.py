# Generated by Django 5.2.4 on 2025-07-15 05:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_transaction_is_cancelled'),
    ]

    operations = [
        migrations.AlterField(
            model_name='balanceitem',
            name='name',
            field=models.CharField(max_length=255, verbose_name='Наименование статьи'),
        ),
    ]
