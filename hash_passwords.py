import os
import django
from django.contrib.auth.hashers import make_password

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'expense_tracker.settings')
django.setup()

from user.models import Registration

def hash_existing_passwords():
    users = Registration.objects.all()
    count = 0
    for user in users:
        # Check if password is already hashed (simple check for Django's default hasher prefix)
        if not user.password.startswith('pbkdf2_sha256$'):
            print(f"Hashing password for user: {user.username}")
            user.password = make_password(user.password)
            # Accessing confirm_password directly. Assuming it exists and holds the plain text password essentially.
            # In a real app, storing confirm_password is bad practice, but since it's here, we hash it.
            user.confirm_password = make_password(user.password) 
            user.save()
            count += 1
        elif not user.confirm_password.startswith('pbkdf2_sha256$'):
             # Handle case where password is hashed but confirm_password isn't (e.g. from previous run)
            print(f"Hashing confirm_password for user: {user.username}")
            user.confirm_password = make_password(user.password) # Sync with password
            user.save()
            count += 1
    
    print(f"Successfully hashed {count} passwords.")

if __name__ == "__main__":
    hash_existing_passwords()
