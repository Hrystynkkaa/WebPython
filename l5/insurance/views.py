from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseForbidden
from .models import User, Policy, Claim
from .forms import UserForm, PolicyForm, ClaimForm

# --- Допоміжні функції ---

def is_admin(request):
    return request.session.get('role') == 'admin'

def get_current_user(request):
    username = request.session.get('username')
    return User.objects.filter(username=username).first()

# --- Аутентифікація ---

def home(request):
    if 'username' not in request.session:
        return redirect('login')
    return render(request, 'index.html')

def login_view(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        role = request.POST.get('role')
        user = User.objects.filter(username=username, role=role).first()
        if user:
            request.session['username'] = user.username
            request.session['role'] = user.role
            return redirect('home')
        return HttpResponse("Невірне ім'я користувача або роль", status=403)
    return render(request, 'login.html')

def logout_view(request):
    request.session.flush()
    return redirect('login')

# --- User Views ---

def user_list(request):
    if not is_admin(request):
        return HttpResponseForbidden("Доступ заборонено")
    users = User.objects.all()
    return render(request, 'user_list.html', {'users': users})

def user_create(request):
    if not is_admin(request):
        return HttpResponseForbidden("Доступ заборонено")
    if request.method == 'POST':
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm()
    return render(request, 'user_form.html', {'form': form})

def user_update(request, user_id):
    if not is_admin(request):
        return HttpResponseForbidden("Доступ заборонено")
    user = get_object_or_404(User, id=user_id)
    if request.method == 'POST':
        form = UserForm(request.POST, instance=user)
        if form.is_valid():
            form.save()
            return redirect('user_list')
    else:
        form = UserForm(instance=user)
    return render(request, 'user_form.html', {'form': form})

def user_delete(request, user_id):
    if not is_admin(request):
        return HttpResponseForbidden("Доступ заборонено")
    user = get_object_or_404(User, id=user_id)
    user.delete()
    return redirect('user_list')

# --- Policy Views ---

def policy_list(request):
    if is_admin(request):
        policies = Policy.objects.all()
    else:
        current_user = get_current_user(request)
        policies = Policy.objects.filter(user=current_user)
    return render(request, 'policy_list.html', {'policies': policies})

def policy_create(request):
    if not is_admin(request):
        return HttpResponseForbidden("Доступ заборонено")
    if request.method == 'POST':
        form = PolicyForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('policy_list')
    else:
        form = PolicyForm()
    return render(request, 'policy_form.html', {'form': form})

def policy_update(request, policy_id):
    if not is_admin(request):
        return HttpResponseForbidden("Доступ заборонено")
    policy = get_object_or_404(Policy, id=policy_id)
    if request.method == 'POST':
        form = PolicyForm(request.POST, instance=policy)
        if form.is_valid():
            form.save()
            return redirect('policy_list')
    else:
        form = PolicyForm(instance=policy)
    return render(request, 'policy_form.html', {'form': form})

def policy_delete(request, policy_id):
    if not is_admin(request):
        return HttpResponseForbidden("Доступ заборонено")
    policy = get_object_or_404(Policy, id=policy_id)
    policy.delete()
    return redirect('policy_list')

# --- Claim Views ---

def claim_list(request):
    if is_admin(request):
        claims = Claim.objects.all()
    else:
        current_user = get_current_user(request)
        claims = Claim.objects.filter(policy__user=current_user)
    return render(request, 'claim_list.html', {'claims': claims})

def claim_create(request):
    if request.method == 'POST':
        form = ClaimForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('claim_list')
        else:
            print(form.errors)
    else:
        form = ClaimForm()

    return render(request, 'create.html', {'form': form})


def claim_update(request, claim_id):
    if not is_admin(request):
        return HttpResponseForbidden("Доступ заборонено")
    claim = get_object_or_404(Claim, id=claim_id)
    if request.method == 'POST':
        form = ClaimForm(request.POST, instance=claim)
        if form.is_valid():
            form.save()
            return redirect('claim_list')
    else:
        form = ClaimForm(instance=claim)
    return render(request, 'claim_form.html', {'form': form})

def claim_delete(request, claim_id):
    if not is_admin(request):
        return HttpResponseForbidden("Доступ заборонено")
    claim = get_object_or_404(Claim, id=claim_id)
    claim.delete()
    return redirect('claim_list')
