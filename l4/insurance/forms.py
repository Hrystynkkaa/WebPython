from django import forms

# Форма для створення/оновлення користувача
class UserForm(forms.Form):
    username = forms.CharField(max_length=100)
    role = forms.ChoiceField(choices=[('user', 'User'), ('admin', 'Admin')])

# Форма для створення страхового полісу
class InsurancePolicyForm(forms.Form):
    policy_name = forms.CharField(max_length=200)
    coverage_amount = forms.IntegerField()
    user_id = forms.CharField(max_length=100)

# Форма для створення заяви на страховий поліс
class ClaimForm(forms.Form):
    claim_amount = forms.IntegerField()
    policy_id = forms.CharField(max_length=100)
