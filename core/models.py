from django.db import models
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _
from decimal import Decimal
import random

# Create your models here.


class BalanceItem(models.Model):
    name = models.CharField(max_length=255, verbose_name="Наименование статьи")
    class Meta:
        verbose_name = "Статья баланса"
        verbose_name_plural = "Статьи баланса"

    def __str__(self):
        return self.name


class BalanceGroup(models.Model):
    item = models.ForeignKey(BalanceItem, on_delete=models.CASCADE, related_name='groups', verbose_name="Статья баланса")
    name = models.CharField(max_length=255, verbose_name="Наименование группы")
    
    class Meta:
        verbose_name = "Балансовые группы"
        verbose_name_plural = "Балансовая группа"

    def __str__(self):
        return f"{self.name} ({self.item.name})"


ACCOUNT_TYPES = [
    ('active', 'Актив'),
    ('passive', 'Пассив'),
    ('both', 'Активно-пассивный'),
]

def generate_account_number():
    return ''.join([str(random.randint(0, 9)) for _ in range(10)])

class Account(models.Model):
    group = models.ForeignKey(BalanceGroup, on_delete=models.CASCADE, related_name='accounts', verbose_name="Балансовая группа")
    number = models.CharField(max_length=10, unique=True, default=generate_account_number,verbose_name="Номер счёта")
    name = models.CharField(max_length=255, verbose_name="Наименование счёта")
    type = models.CharField(max_length=10, choices=ACCOUNT_TYPES, verbose_name="Тип счёта")
    balance = models.DecimalField(max_digits=18, decimal_places=2, default=0, verbose_name="Баланс")

    def __str__(self):
        return f"{self.number} - {self.name}"


class Transaction(models.Model):
    debit_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='debit_transactions', verbose_name="Дебет")
    credit_account = models.ForeignKey(Account, on_delete=models.CASCADE, related_name='credit_transactions', verbose_name="Кредит")
    amount = models.DecimalField(max_digits=18, decimal_places=2, verbose_name="Сумма")
    description = models.TextField(blank=True, verbose_name="Описание")
    created_at = models.DateTimeField(auto_now_add=True,verbose_name="Дата и время")
    is_cancelled = models.BooleanField(default=False, verbose_name="Аннулирована")

    def clean(self):
        errors = {}
    
        if self.amount is None:
            errors['amount'] = 'Поле "Сумма" обязательно.'
        elif self.amount <= Decimal('0.00'):
            errors['amount'] = 'Сумма должна быть больше нуля.'
    
        if self.debit_account_id and self.credit_account_id:
            if self.debit_account_id == self.credit_account_id:
                errors['debit_account'] = 'Счета дебета и кредита не могут совпадать.'
        else:
            errors['debit_account'] = 'Укажите дебет и кредит.'
    
        if errors:
            raise ValidationError(errors)

    def save(self, *args, **kwargs):
        is_new = self.pk is None
        self.full_clean()
        super().save(*args, **kwargs)
        if is_new:
            self.apply_double_entry()

    def apply_double_entry(self):
        print("=== APPLY DOUBLE ENTRY ===")

        print(f"до: дебет {self.debit_account.name}: {self.debit_account.balance}")
        print(f"до: кредит {self.credit_account.name}: {self.credit_account.balance}")

        self.debit_account.balance += self.amount
        self.credit_account.balance -= self.amount

        print(f"после: дебет {self.debit_account.name}: {self.debit_account.balance}")
        print(f"после: кредит {self.credit_account.name}: {self.credit_account.balance}")

        self.debit_account.save(update_fields=["balance"])
        self.credit_account.save(update_fields=["balance"])


    def cancel(self):
        if self.is_cancelled:
            raise ValidationError("Транзакция уже отменена.")

    # Метка что транзакция отменена
        self.is_cancelled = True
        self.save(update_fields=['is_cancelled'])

        reversed_transaction = Transaction.objects.create(
            debit_account=self.credit_account,    
            credit_account=self.debit_account,    
            amount=self.amount,
            description=f"Отмена транзакции #{self.id}",
    )
        return reversed_transaction

    
    



    