# insurance_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),

    # Маршрути для користувачів
    path('users/', views.user_list, name='user_list'),
    path('users/create/', views.user_create, name='user_create'),
    path('users/<int:user_id>/edit/', views.user_update, name='user_update'),
    path('users/<int:user_id>/delete/', views.user_delete, name='user_delete'),

    # Маршрути для страхових полісів
    path('policies/', views.policy_list, name='policy_list'),
    path('policies/create/', views.policy_create, name='policy_create'),
    path('policies/<int:policy_id>/edit/', views.policy_update, name='policy_update'),
    path('policies/<int:policy_id>/delete/', views.policy_delete, name='policy_delete'),

    # Маршрути для заяв
    path('claims/', views.claim_list, name='claim_list'),
    path('claims/create/', views.claim_create, name='claim_create'),
    path('claims/<int:claim_id>/edit/', views.claim_update, name='claim_update'),
    path('claims/<int:claim_id>/delete/', views.claim_delete, name='claim_delete'),
]

