from unicodedata import category
from django.db import models # type: ignore


class Registration(models.Model):

    ROLE_CHOICES = (
        ('user', 'User'),
        ('family', 'Family Member'),
    )

    username = models.CharField(max_length=100, unique=True)
    password = models.CharField(max_length=100)
    email_id = models.EmailField()
    phn_no = models.CharField(max_length=15)
    location = models.CharField(max_length=100)
    role = models.CharField(max_length=10, choices=ROLE_CHOICES)

    parent = models.ForeignKey(
        "self",
        null=True,
        blank=True,
        on_delete=models.CASCADE,
        related_name="family_members"
    )

    otp = models.CharField(max_length=6, blank=True, null=True)


class Notification(models.Model):
    time = models.CharField(max_length=50)
    date = models.DateField() 
    send_by = models.EmailField(max_length=50)
    send_to = models.EmailField(max_length=50)
    Description = models.CharField(max_length=50)

class Category(models.Model):
    category_type = models.CharField(max_length=100)

    def __str__(self):
        return self.category_type
    
    
class Transaction(models.Model):
    date = models.DateField()
    category_id = models.ForeignKey('Category', on_delete=models.CASCADE)
    amount = models.FloatField()
    Transaction_desc = models.CharField(max_length=100)
    Type = models.CharField(max_length=100)

    by = models.ForeignKey(
        Registration,
        related_name="transaction",
        on_delete=models.PROTECT
    )  
    # values: 'user' or 'family'
    



    
     
class Reminder(models.Model):
    date = models.DateField()
    time = models.CharField(max_length=50)
    Reminder_desc = models.CharField(max_length=100)
    Email_id = models.EmailField(max_length=100)

    by = models.ForeignKey(
        Registration,
        related_name="reminder",
        on_delete=models.PROTECT,
    )


