from django import forms # type: ignore
from . models import Registration, Notification, Transaction, Category, Reminder

class RegistrationForm(forms.ModelForm):
    class Meta: 
        model=Registration
        fields=['Registration_id',
                'username',
                'password',
                'confirm_password',
                'email_id',
                'phn_no',
                'location',
                ]
        
        widgets = {
            'email_id': forms.EmailInput(attrs={
                "placeholder": "Enter your email",
                "class": "form-control",
            }),#Customized Email

            'Registration_id': forms.NumberInput(attrs={
                "placeholder": "Enter your id",
                "class": "form-control",
            }),
            'username': forms.TextInput(attrs={
                "placeholder": "Enter your username",  #class referes to css class yet not implimented
                "class": "form-control",
            }),#Customized text input

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
                "class": "form-control"

        })
            
        }
        
       
     

class NotificationForm(forms.ModelForm):
    class Meta: 
        model=Notification
        fields=['id',
                'time',
                'date',
                'send_by',
                'send_to',
                'Description']  

class TransactionForm(forms.ModelForm):
    class Meta: 
        model=Transaction
        fields=['id',
                'date',
                'amount',
                'category_id',
                'Registration_id',
                'Transaction_desc',
                'Type']  

        labels = {
            'category_id': 'Category',
            'Registration_id':'Spend by',
            'Type':'Type of Transaction',
             }
        
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),   #this will render date picker
              
            
            
            'Type': forms.TextInput(attrs={
                "placeholder": "Enter type of transaction",
                "class": "form-control",
            }),
            'amount': forms.NumberInput(attrs={
                "placeholder": "Enter amount",
                "class": "form-control",
            }),
            'id': forms.NumberInput(attrs={
                "placeholder": "Enter Transaction id",
                "class": "form-control",
            }),
            'Transaction_desc': forms.TextInput(attrs={
                "placeholder": "Enter Transaction description",
                "class": "form-control",
            }),
        } 
            
            

class CategoryForm(forms.ModelForm):
    class Meta: 
        model=Category
        fields=['category_id',
                'category_type']
        
        widgets = {
            'category_id': forms.NumberInput(attrs={
                "placeholder":"Enter category id",
                "class": "form-control", 
            }),
            'category_type': forms.TextInput(attrs={
                "placeholder":"Enter category type",
                "class": "form-control", 
            }),
        }
    
        

class ReminderForm(forms.ModelForm):
    class Meta: 
        model=Reminder
        fields=['date',
                'time',
                'Reminder_desc',
                'Email_id']  
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),   #this will render date picker
            'time': forms.TimeInput(attrs={'type': 'time'}),
            'Reminder_desc': forms.TextInput(attrs={
                "placeholder":"Enter description",
                "class": "form-control", 
            }),
            'Email_id': forms.EmailInput(attrs={
                "placeholder":"Enter email",
                "class": "form-control", 
            }),
              
        }



class LoginForm(forms.ModelForm):
    class Meta: 
        model=Registration
        fields=['username',
                'password'] 
        widgets = {
            'password': forms.PasswordInput(attrs={
                "placeholder":"Enter password",
                "class": "form-control", 
            }),
            'username': forms.TextInput(attrs={
                "placeholder":"Enter username",
                "class": "form-control", 
            }),
        }          





class DashboardForm(forms.ModelForm):
    class Meta:
        model=Transaction
        fields=[]

class ResetForm(forms.ModelForm):
    class Meta:
        model=Registration
        fields=['email_id',
                'password',
                'confirm_password'] 
        widgets = {
            
            'password': forms.PasswordInput(attrs={
                "placeholder":"Enter password",
                "class": "form-control", 
            }),
            'username': forms.TextInput(attrs={
                "placeholder":"Enter username",
                "class": "form-control", 
            }),
            'email_id': forms.EmailInput(attrs={
                "placeholder":"Enter email",
                "class": "form-control", 
            }),
        }      
        
        




        

        
    