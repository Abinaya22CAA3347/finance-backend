from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth import authenticate
from .models import User, Transaction
from .serializers import UserSerializer, RegisterSerializer, TransactionSerializer
from django.db.models import Sum

# Permission Classes
class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role == 'admin'

class IsAnalystOrAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.role in ['admin', 'analyst']

# Register View
class RegisterView(generics.CreateAPIView):
    queryset = User.objects.all()
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

# Login View
class LoginView(APIView):
    permission_classes = [permissions.AllowAny]

    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            return Response({
                'refresh': str(refresh),
                'access': str(refresh.access_token),
                'role': user.role
            })
        return Response({'error': 'Invalid credentials'}, status=400)

# User List View (Admin only)
class UserListView(generics.ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [permissions.IsAuthenticated, IsAdmin]

# Transaction Views
class TransactionListCreateView(generics.ListCreateAPIView):
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        queryset = Transaction.objects.all()
        category = self.request.query_params.get('category')
        type = self.request.query_params.get('type')
        date = self.request.query_params.get('date')
        if category:
            queryset = queryset.filter(category=category)
        if type:
            queryset = queryset.filter(type=type)
        if date:
            queryset = queryset.filter(date=date)
        return queryset

    def perform_create(self, serializer):
        if self.request.user.role == 'viewer':
            raise permissions.PermissionDenied("Viewers cannot create transactions")
        serializer.save(user=self.request.user)

class TransactionDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer
    permission_classes = [permissions.IsAuthenticated]

    def update(self, request, *args, **kwargs):
        if request.user.role == 'viewer':
            raise permissions.PermissionDenied("Viewers cannot update transactions")
        return super().update(request, *args, **kwargs)

    def destroy(self, request, *args, **kwargs):
        if request.user.role != 'admin':
            raise permissions.PermissionDenied("Only admin can delete transactions")
        return super().destroy(request, *args, **kwargs)

# Dashboard Summary View
class DashboardView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request):
        transactions = Transaction.objects.all()
        total_income = transactions.filter(type='income').aggregate(Sum('amount'))['amount__sum'] or 0
        total_expense = transactions.filter(type='expense').aggregate(Sum('amount'))['amount__sum'] or 0
        net_balance = total_income - total_expense
        category_totals = transactions.values('category').annotate(total=Sum('amount'))
        recent = TransactionSerializer(transactions.order_by('-created_at')[:5], many=True).data

        return Response({
            'total_income': total_income,
            'total_expense': total_expense,
            'net_balance': net_balance,
            'category_totals': list(category_totals),
            'recent_transactions': recent
        })