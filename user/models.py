from unicodedata import category
from django.db import models # type: ignore

class Registration(models.Model):
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=100)
    confirm_password = models.CharField(max_length=100)
    email_id = models.EmailField()
    phn_no = models.CharField(max_length=15)
    location = models.CharField(max_length=100)

    ROLE_CHOICES = (
        ('user', 'User'),
        ('family', 'Family Member'),
    )

    role = models.CharField(max_length=10, choices=ROLE_CHOICES)


class Notification(models.Model):
    id = models.IntegerField(max_length=20,primary_key=True)
    time = models.CharField(max_length=50)
    date = models.DateField() 
    send_by = models.EmailField(max_length=50)
    send_to = models.EmailField(max_length=50)
    Description = models.CharField(max_length=50)

class Transaction(models.Model):
     id = models.IntegerField(max_length=20,primary_key=True)
     date = models.DateField()
     category_id = models.ForeignKey(
         'Category',
         on_delete=models.CASCADE,
         related_name='Categories')
     
     amount = models.FloatField(max_length=100)
     Transaction_desc = models.CharField(max_length=100)
     Type = models.CharField(max_length=100)

     def __str__(self):
        return self.Type
     

class  Category(models.Model):
    category_id = models.IntegerField(max_length=50,primary_key=True)   
    category_type = models.CharField(max_length=100) 

    def __str__(self):
        return self.category_type
    
     
class Reminder(models.Model):
    date = models.DateField()
    time = models.CharField(max_length=50)
    Reminder_desc = models.CharField(max_length=100)
    Email_id = models.EmailField(max_length=100)


