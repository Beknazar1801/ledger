from django.shortcuts import render, redirect, get_object_or_404
from .models import Account, Transaction
from .forms import TransactionForm
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.views.decorators.http import require_POST

def account_list(request):
    accounts = Account.objects.select_related('group', 'group__item')
    return render(request, 'core/accounts.html', {'accounts': accounts})

def create_transaction(request):
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('transactions')
    else:
        form = TransactionForm()
    return render(request, 'core/transaction_form.html', {'form': form})

def transaction_list(request):
    transactions = Transaction.objects.select_related('debit_account', 'credit_account').order_by('-created_at')
    return render(request, 'core/transactions.html', {'transactions': transactions})

@require_POST
def cancel_transaction(request, transaction_id):
    transaction = get_object_or_404(Transaction, pk=transaction_id)

    try:
        transaction.cancel()
        messages.success(request, f'Транзакция #{transaction_id} успешно отменена.')
    except ValidationError as e:
        # Если ValidationError, получаем ошибки в readable формате
        error_messages = []
        if hasattr(e, 'message_dict'):
            for field, errors in e.message_dict.items():
                error_messages.extend(errors)
        else:
            error_messages.append(str(e))
        messages.error(request, 'Ошибка отмены транзакции: ' + '; '.join(error_messages))

    return redirect('transactions')  # Имя url с историей транзакций

