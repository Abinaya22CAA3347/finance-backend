from django.urls import path
from .views import (
    RegisterView, LoginView, UserListView,
    TransactionListCreateView, TransactionDetailView,
    DashboardView
)
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    # Auth
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

    # Users
    path('users/', UserListView.as_view(), name='user-list'),

    # Transactions
    path('transactions/', TransactionListCreateView.as_view(), name='transaction-list'),
    path('transactions/<int:pk>/', TransactionDetailView.as_view(), name='transaction-detail'),

    # Dashboard
    path('dashboard/', DashboardView.as_view(), name='dashboard'),
]