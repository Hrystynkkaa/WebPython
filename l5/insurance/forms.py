from django import forms
from .models import User, Policy, Claim

# Форма для користувача
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'role']
        widgets = {
            'role': forms.Select(choices=User.ROLE_CHOICES)
        }

# Форма для страхового полісу
class PolicyForm(forms.ModelForm):
    class Meta:
        model = Policy
        fields = ['user', 'coverage']
        widgets = {
            'user': forms.Select(),
        }

# Форма для заяви
class ClaimForm(forms.ModelForm):
    class Meta:
        model = Claim
        fields = ['policy', 'amount']
        widgets = {
            'policy': forms.Select(),
        }
