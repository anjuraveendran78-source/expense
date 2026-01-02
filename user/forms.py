from django import forms
from .models import Registration, Notification, Transaction, Category, Reminder


# ===================== REGISTRATION FORM =====================

class RegistrationForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['username', 'password', 'confirm_password', 'email_id', 'phn_no', 'location']


        widgets = {
            'email_id': forms.EmailInput(attrs={
                "placeholder": "Enter your email",
                "class": "form-control",
            }),

            'username': forms.TextInput(attrs={
                "placeholder": "Enter your username",
                "class": "form-control",
            }),

            'location': forms.TextInput(attrs={
                "placeholder": "Enter your Location",
                "class": "form-control",
            }),

            'password': forms.PasswordInput(attrs={
                "placeholder": "Enter password",
                "class": "form-control",
            }),

            'confirm_password': forms.PasswordInput(attrs={
                "placeholder": "Enter password again",
                "class": "form-control",
            }),

            'phn_no': forms.NumberInput(attrs={
                "placeholder": "Enter phone number",
                "class": "form-control",
            }),
        }


# ===================== LOGIN FORM =====================

class LoginForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['username', 'password']

        widgets = {
            'password': forms.PasswordInput(attrs={
                "placeholder": "Enter password",
                "class": "form-control",
            }),
            'username': forms.TextInput(attrs={
                "placeholder": "Enter username",
                "class": "form-control",
            }),
        }


# ===================== TRANSACTION FORM =====================

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['date', 'amount', 'category_id', 'Transaction_desc', 'Type']

        labels = {
            'category_id': 'Category',
            'Type': 'Type of Transaction',
        }

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),

            'Type': forms.Select(choices=[
                ('Income', 'Income'),
                ('Expense', 'Expense')
            ], attrs={
                'class': 'form-control'
            }),

            'amount': forms.NumberInput(attrs={
                'placeholder': 'Enter amount',
                'class': 'form-control',
            }),

            'Transaction_desc': forms.TextInput(attrs={
                'placeholder': 'Enter transaction description',
                'class': 'form-control',
            }),
        }



# ===================== CATEGORY FORM =====================

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_id', 'category_type']

        widgets = {
            'category_id': forms.NumberInput(attrs={
                "placeholder": "Enter category id",
                "class": "form-control",
            }),
            'category_type': forms.TextInput(attrs={
                "placeholder": "Enter category type",
                "class": "form-control",
            }),
        }


# ===================== REMINDER FORM =====================

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['date', 'time', 'Reminder_desc', 'Email_id']

        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'Reminder_desc': forms.TextInput(attrs={
                "placeholder": "Enter description",
                "class": "form-control",
            }),
            'Email_id': forms.EmailInput(attrs={
                "placeholder": "Enter email",
                "class": "form-control",
            }),
        }


# ===================== DASHBOARD FORM =====================

class DashboardForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = []


# ===================== RESET PASSWORD FORM =====================

class ResetForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['email_id', 'password', 'confirm_password']

        widgets = {
            'password': forms.PasswordInput(attrs={
                "placeholder": "Enter password",
                "class": "form-control",
            }),
            'email_id': forms.EmailInput(attrs={
                "placeholder": "Enter email",
                "class": "form-control",
            }),
        }


# ===================== NOTIFICATION FORM =====================

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['id', 'time', 'date', 'send_by', 'send_to', 'Description']
