from django import forms
from .models import Registration, Notification, Transaction, Category, Reminder


# ===================== REGISTRATION FORM =====================

# ===================== REGISTRATION FORM =====================

from django import forms
from .models import Registration
from django.contrib.auth.hashers import make_password


class RegistrationForm(forms.ModelForm):
    confirm_password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            "placeholder": "Confirm password",
            "class": "w-full px-4 py-3 rounded-lg bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-700 text-slate-900 dark:text-white focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all placeholder-gray-400 dark:placeholder-slate-500",
        })
    )

    class Meta:
        model = Registration
        fields = ['username', 'email_id', 'phn_no', 'location', 'password']

        widgets = {

            'username': forms.TextInput(attrs={
                "placeholder": "Enter your username",
                "class": "w-full px-4 py-3 rounded-lg bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-700 text-slate-900 dark:text-white focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all placeholder-gray-400 dark:placeholder-slate-500",
            }),

            'email_id': forms.EmailInput(attrs={
                "placeholder": "Enter your email",
                "class": "w-full px-4 py-3 rounded-lg bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-700 text-slate-900 dark:text-white focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all placeholder-gray-400 dark:placeholder-slate-500",
            }),

            'location': forms.TextInput(attrs={
                "placeholder": "Enter your Location",
                "class": "w-full px-4 py-3 rounded-lg bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-700 text-slate-900 dark:text-white focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all placeholder-gray-400 dark:placeholder-slate-500",
            }),

            'password': forms.PasswordInput(attrs={
                "placeholder": "Enter password",
                "class": "w-full px-4 py-3 rounded-lg bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-700 text-slate-900 dark:text-white focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all placeholder-gray-400 dark:placeholder-slate-500",
            }),

            'phn_no': forms.TextInput(attrs={   
                "placeholder": "Enter phone number",
                "class": "w-full px-4 py-3 rounded-lg bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-700 text-slate-900 dark:text-white focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all placeholder-gray-400 dark:placeholder-slate-500",
            }),
        }

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get("password")
        confirm_password = cleaned_data.get("confirm_password")

        if password != confirm_password:
            raise forms.ValidationError("Passwords do not match")

        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.password = make_password(self.cleaned_data["password"])
        user.role = "user"
        if commit:
            user.save()
        return user



# ===================== LOGIN FORM =====================

class LoginForm(forms.ModelForm):
    class Meta:
        model = Registration
        fields = ['username', 'password']

        widgets = {
            'password': forms.PasswordInput(attrs={
                "placeholder": "Enter password",
                "class": "w-full px-4 py-3 rounded-lg bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-700 text-slate-900 dark:text-white focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all placeholder-gray-400 dark:placeholder-slate-500",
            }),
            'username': forms.TextInput(attrs={
                "placeholder": "Enter username",
                "class": "w-full px-4 py-3 rounded-lg bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-700 text-slate-900 dark:text-white focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all placeholder-gray-400 dark:placeholder-slate-500",
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
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-3 rounded-xl bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-600 text-slate-900 dark:text-white focus:ring-2 focus:ring-indigo-500 outline-none transition-all'
            }),

            'category_id': forms.Select(attrs={
                'class': 'w-full px-4 py-3 rounded-xl bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-600 text-slate-900 dark:text-white focus:ring-2 focus:ring-indigo-500 outline-none transition-all'
            }),

            'Type': forms.Select(choices=[
                ('Income', 'Income'),
                ('Expense', 'Expense')
            ], attrs={
                'class': 'hidden' # Visual toggle handles this in template, but keep hidden input
            }),

            'amount': forms.NumberInput(attrs={
                'placeholder': 'Enter amount',
                'class': 'w-full pl-8 pr-4 py-3 rounded-xl bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-600 text-slate-900 dark:text-white focus:ring-2 focus:ring-emerald-500 outline-none transition-all',
            }),

            'Transaction_desc': forms.TextInput(attrs={
                'placeholder': 'Enter transaction description',
                'class': 'w-full px-4 py-3 rounded-xl bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-600 text-slate-900 dark:text-white focus:ring-2 focus:ring-indigo-500 outline-none transition-all',
            }),
        }



# ===================== CATEGORY FORM =====================

class CategoryForm(forms.ModelForm):
    class Meta:
        model = Category
        fields = ['category_type']

        widgets = {
            'category_type': forms.TextInput(attrs={
                "placeholder": "Enter category type",
                "class": "w-full px-4 py-3 rounded-xl bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-600 text-slate-900 dark:text-white focus:ring-2 focus:ring-blue-500 outline-none transition-all placeholder-gray-400 dark:placeholder-slate-500",
            }),
        }


# ===================== REMINDER FORM =====================

class ReminderForm(forms.ModelForm):
    class Meta:
        model = Reminder
        fields = ['date', 'time', 'Reminder_desc', 'Email_id']

        widgets = {
            'date': forms.DateInput(attrs={
                'type': 'date',
                'class': 'w-full px-4 py-3 rounded-xl bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-600 text-slate-900 dark:text-white focus:ring-2 focus:ring-indigo-500 outline-none transition-all'
            }),
            'time': forms.TimeInput(attrs={
                'type': 'time',
                'class': 'w-full px-4 py-3 rounded-xl bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-600 text-slate-900 dark:text-white focus:ring-2 focus:ring-indigo-500 outline-none transition-all'
            }),
            'Reminder_desc': forms.TextInput(attrs={
                "placeholder": "Enter description",
                "class": "w-full px-4 py-3 rounded-xl bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-600 text-slate-900 dark:text-white focus:ring-2 focus:ring-indigo-500 outline-none transition-all h-24 resize-none",
            }),
            'Email_id': forms.EmailInput(attrs={
                "placeholder": "Enter email",
                "class": "w-full px-4 py-3 rounded-xl bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-600 text-slate-900 dark:text-white focus:ring-2 focus:ring-indigo-500 outline-none transition-all placeholder-gray-400 dark:placeholder-slate-500",
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
        fields = ['email_id', 'password']

        widgets = {
            'password': forms.PasswordInput(attrs={
                "placeholder": "Enter password",
                "class": "w-full px-4 py-3 rounded-lg bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-700 text-slate-900 dark:text-white focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all placeholder-gray-400 dark:placeholder-slate-500",
            }),
            'email_id': forms.EmailInput(attrs={
                "placeholder": "Enter email",
                "class": "w-full px-4 py-3 rounded-lg bg-gray-50 dark:bg-slate-900 border border-gray-200 dark:border-slate-700 text-slate-900 dark:text-white focus:ring-2 focus:ring-emerald-500 focus:border-transparent outline-none transition-all placeholder-gray-400 dark:placeholder-slate-500",
            }),
        }


# ===================== NOTIFICATION FORM =====================

class NotificationForm(forms.ModelForm):
    class Meta:
        model = Notification
        fields = ['id', 'time', 'date', 'send_by', 'send_to', 'Description']
