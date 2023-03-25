from django.urls import path
from . import views


urlpatterns = [
    path('splitwise/auth/', views.splitwise_auth, name='splitwise_auth'),
    # Add more URL patterns as needed
    path('', views.home, name='splitWise-home'),
    path('splitwise/oauth/callback/', views.splitwise_oauth_callback, name='splitwise_oauth_callback'),
    # path('splitwise/friends/', views.splitwise_friends, name='splitwise_friends'),
    path('splitwise/groups/', views.groups, name='groups'),
    path('groups/<int:group_id>/', views.get_group, name='get_group'),
    path('group/<int:group_id>/add_expense/', views.add_expense, name='add_expense'),
    path('group/<int:group_id>/add_expense_normal/', views.add_expense_normal, name='add_expense_normal'),
    path('expense/<int:expense_id>/', views.expense_details, name='expense_details'),
]
