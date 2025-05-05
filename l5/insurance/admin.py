from django.contrib import admin
from .models import User, Policy, Claim

admin.site.register(User)
admin.site.register(Policy)
admin.site.register(Claim)
