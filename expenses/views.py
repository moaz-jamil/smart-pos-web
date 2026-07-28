from decimal import Decimal
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from expenses.models import Expense, ExpenseCategory

@login_required
def expenses_list(request):
    business = request.user.business
    expenses = Expense.objects.filter(business=business).order_by('-expense_date') if business else Expense.objects.all().order_by('-expense_date')
    categories = ExpenseCategory.objects.filter(business=business) if business else ExpenseCategory.objects.all()

    if request.method == 'POST':
        title = request.POST.get('title')
        category_id = request.POST.get('category')
        amount = Decimal(request.POST.get('amount', '0.00'))
        expense_date = request.POST.get('expense_date')
        notes = request.POST.get('notes', '')

        if title and category_id and amount:
            cat = ExpenseCategory.objects.get(pk=category_id)
            Expense.objects.create(
                business=business,
                branch=request.user.branch,
                category=cat,
                title=title,
                amount=amount,
                expense_date=expense_date,
                notes=notes
            )
            messages.success(request, f"Expense '{title}' logged successfully.")
            return redirect('expenses_list')

    return render(request, 'expenses/expenses_list.html', {'expenses': expenses, 'categories': categories})


@login_required
def expense_categories(request):
    business = request.user.business
    categories = ExpenseCategory.objects.filter(business=business) if business else ExpenseCategory.objects.all()

    if request.method == 'POST':
        name = request.POST.get('name')
        desc = request.POST.get('description', '')
        if name:
            ExpenseCategory.objects.create(business=business, name=name, description=desc)
            messages.success(request, f"Category '{name}' added.")
            return redirect('expense_categories')

    return render(request, 'expenses/expense_categories.html', {'categories': categories})
