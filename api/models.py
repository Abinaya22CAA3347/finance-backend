from django.contrib.auth.models import AbstractUser
from django.db import models

# User Model with Roles
class User(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('analyst', 'Analyst'),
        ('viewer', 'Viewer'),
    )
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='viewer')
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.username} ({self.role})"


# Financial Transaction Model
class Transaction(models.Model):
    TYPE_CHOICES = (
        ('income', 'Income'),
        ('expense', 'Expense'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=10, choices=TYPE_CHOICES)
    category = models.CharField(max_length=50)
    date = models.DateField()
    notes = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.type} - {self.amount} ({self.category})"