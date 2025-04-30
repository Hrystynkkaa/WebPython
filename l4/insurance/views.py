# insurance_app/views.py
from django.shortcuts import render, redirect
from django.http import HttpResponse
from .data import User, users, Policy, policies, Claim, claims

# Головна сторінка
def home(request):
    return render(request, 'index.html')

# ========== Представлення для КОРИСТУВАЧІВ ==========
def user_list(request):
    return render(request, 'user_list.html', {'users': users})

def user_create(request):
    if request.method == 'POST':
        name = request.POST.get('username')  # Ім'я
        role = request.POST.get('role')  # Роль
        new_id = max((u.id for u in users), default=0) + 1
        users.append(User(new_id, name, role))  # Створюємо користувача без email
        return redirect('user_list')
    return render(request, 'user_form.html')

def user_update(request, user_id):
    user = next((u for u in users if u.id == user_id), None)
    if not user:
        return HttpResponse('User not found', status=404)
    if request.method == 'POST':
        user.name = request.POST.get('name')  # Оновлюємо ім'я
        user.role = request.POST.get('role')  # Оновлюємо роль
        return redirect('user_list')
    return render(request, 'user_form.html', {'user': user})

def user_delete(request, user_id):
    user = next((u for u in users if u.id == user_id), None)
    if user:
        users.remove(user)
    return redirect('user_list')


# ========== Представлення для ПОЛІСІВ ==========
def policy_list(request):
    return render(request, 'policy_list.html', {'policies': policies})

def policy_create(request):
    if request.method == 'POST':
        user_id = int(request.POST.get('user_id'))
        coverage = float(request.POST.get('coverage'))
        new_id = max((p.id for p in policies), default=0) + 1
        policies.append(Policy(new_id, user_id, coverage))
        return redirect('policy_list')
    return render(request, 'policy_form.html', {'users': users})

def policy_update(request, policy_id):
    policy = next((p for p in policies if p.id == policy_id), None)
    if not policy:
        return HttpResponse('Policy not found', status=404)
    if request.method == 'POST':
        policy.user_id = int(request.POST.get('user_id'))
        policy.coverage = float(request.POST.get('coverage'))
        return redirect('policy_list')
    return render(request, 'policy_form.html', {'policy': policy, 'users': users})

def policy_delete(request, policy_id):
    policy = next((p for p in policies if p.id == policy_id), None)
    if policy:
        policies.remove(policy)
    return redirect('policy_list')


# ========== Представлення для ЗАЯВ ==========
def claim_list(request):
    return render(request, 'claim_list.html', {'claims': claims})

def claim_create(request):
    if request.method == 'POST':
        policy_id = int(request.POST.get('policy_id'))
        amount = float(request.POST.get('amount'))
        new_id = max((c.id for c in claims), default=0) + 1
        claims.append(Claim(new_id, policy_id, amount))
        return redirect('claim_list')
    return render(request, 'claim_form.html', {'users': users, 'policies': policies})


def claim_update(request, claim_id):
    claim = next((c for c in claims if c.id == claim_id), None)
    if not claim:
        return HttpResponse('Claim not found', status=404)

    if request.method == 'POST':
        # Оновлення суми
        amount = request.POST.get('amount')
        if amount:
            claim.amount = float(amount)  # Приведення до числа з плаваючою точкою

        # Оновлення ID поліса
        policy_id = request.POST.get('policy_id')
        if policy_id:
            claim.policy_id = int(policy_id)

        return redirect('claim_list')  # Переадресація на список заяв

    # Виведення форми для редагування
    return render(request, 'claim_form.html', {'claim': claim, 'users': users, 'policies': policies})


def claim_delete(request, claim_id):
    claim = next((c for c in claims if c.id == claim_id), None)
    if claim:
        claims.remove(claim)
    return redirect('claim_list')
