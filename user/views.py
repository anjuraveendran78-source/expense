from django.http import HttpResponse # type: ignore
from django .shortcuts import render,redirect,get_object_or_404 # type: ignore
from .models import Registration, Notification, Transaction, Category, Reminder
from .forms import LoginForm, RegistrationForm,TransactionForm,DashboardForm,ResetForm,CategoryForm,ReminderForm
from django.contrib.auth.hashers import make_password, check_password
# from .util import get_phonepe_client,meta_info_generation,buil_request
from django.urls import reverse
from uuid import uuid4

import random
from django.db.models import Sum, Q
from django.db.models.functions import TruncMonth
import json
from django.utils.dateformat import DateFormat
from django.utils.formats import get_format
from django.shortcuts import render
from django.template.loader import get_template
from xhtml2pdf import pisa
from django.contrib import messages
from datetime import datetime, timedelta
from django.conf import settings
from django.db import IntegrityError
from django.core.mail import send_mail
from .util import send_email
from django.utils.timezone import now

#BASIC Page Renders

def main_home(request):
    return render(request, 'home.html')

def login_page(request):
    register=LoginForm
    return render(request, 'login.html', {
        'forms':register,})

def Register_page(request):
    Register=RegistrationForm()
    return render(request, 'registration.html',{'forms':Register})

def UserHome_page(request):
    role = request.session.get('role')
    return render(request, 'userhome.html',
                  {'role':role}
                  )

def FamHome_page(request):
    return render(request, 'famhome.html')

def Expense_page(request):
    role = request.session.get('role')
    Expense=TransactionForm()
    return render(request, 'expense.html', {
        'forms':Expense,
        'role':role})

def Dashboard1_page(request):
    user_id = request.session.get('user_id')
    if not user_id:
        return redirect('user_login_page')
    
    user = get_object_or_404(Registration, id=user_id)
    role = user.role
    
    # Fetch transactions
    transactions = Transaction.objects.filter(by=user).order_by('-date')
    
    # Calculate totals
    income = transactions.filter(Type__icontains="income").aggregate(total=Sum("amount"))["total"] or 0
    expense = transactions.filter(Type__icontains="expense").aggregate(total=Sum("amount"))["total"] or 0
    balance = income - expense
    
    # Recent transactions (last 5)
    recent_transactions = transactions[:5]
    
    context = {
        'role': role,
        'user': user,
        'income_total': income,
        'expense_total': expense,
        'balance': balance,
        'transactions': recent_transactions,
        'forms': DashboardForm() # Keep existing form just in case
    }
    
    return render(request, 'dashboard1.html', context)

def Dashboard2_page(request):
    Dashboard2=DashboardForm()
    return render(request, 'dashboard2.html', {'forms':Dashboard2})

def Reset_page(request):
    Reset_password=ResetForm()
    return render(request, 'passwordreset.html', {'forms':Reset_password})

def Familyexpense_page(request):
    Family_Expense=TransactionForm()
    return render(request, 'familyexpense.html', {'forms':Family_Expense})

def Category_page(request):
    category= CategoryForm()
    role = request.session.get('role')
    return render(request, 'category.html', {
        'forms':category,
        'role':role
        })

def Familyreg_page(request):
    familyregister=RegistrationForm()
    role = request.session.get('role')
    return render(request, 'familyreg.html',{
        'forms':familyregister,
        'role':role})

def Reminder1_page(request):
    reminder1 = ReminderForm()
    role = request.session.get('role')
    return render(request, 'reminder1.html', {
        'forms':reminder1,
        'role':role,})

def Reminder2_page(request):
    reminder2 = ReminderForm()
    role = request.session.get('role')
    return render(request, 'reminder2.html', {
        'forms':reminder2,
        'role':role})

def reminder_list1(request):
    user = request.session.get("user_id")
    logged_user = get_object_or_404(Registration,id=user)
    reminders = Reminder.objects.filter(by=logged_user)
    role = request.session.get('role')
    return render(request, 'reminder_list1.html', {
        'reminders': reminders,
        'role':role})

def reminder_list2(request):
    reminders = Reminder.objects.filter(owner_type='family')
    role = request.session.get('role')
    return render(request, 'reminder_list2.html', {
        'reminders': reminders,
        'role':role})


# Login Action Page

def user_login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        
        # Get user by username first
        user = Registration.objects.filter(username=username).first()
        
        # Verify password hash
        if user and check_password(password, user.password):
            request.session["username"] = user.username
            request.session["user_id"] = user.id
            request.session["role"] = user.role
            if user.role == "user":
                return redirect("UserHome_page")
            else:
                return redirect("FamHome_page")
        else:
            messages.error(request,"invalid user name or password")
            return redirect('login_page')
    
    return render(request, "login.html")

#User Registration Action Pages

def user_reg1_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        email_id = request.POST.get("email_id")
        phn_no = request.POST.get("phn_no")
        location = request.POST.get("location")

        if password != confirm_password:
            messages.error(request, "Passwords do not match")
            return redirect("Register_page")

        try:
            Registration.objects.create(
                username=username,
                password=make_password(password),
                email_id=email_id,
                phn_no=phn_no,
                location=location,
                role="user"
            )

            subject = "Registration confirmation"
            body = "Thank you for registering with us"
            send_email(email_id, subject, body)

        except IntegrityError:
            messages.error(request, "Username already exists")
            return redirect("Register_page")

        return redirect("user_login_page")

    return render(request, "user/user_register.html")


#family member Registration Action Pages

def user_reg2_page(request):

    if request.method == "POST":

        logged_user_id = request.session.get("user_id")
        if not logged_user_id:
            return redirect("user_login_page")

        parent_user = Registration.objects.get(id=logged_user_id)

        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        email_id = request.POST.get("email_id")
        phn_no = request.POST.get("phn_no")
        location = request.POST.get("location")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
            return redirect("Familyreg_page")

        if Registration.objects.filter(username=username).exists():
            messages.error(request, "Username already exists.")
            return redirect("Familyreg_page")

        if Registration.objects.filter(email_id=email_id).exists():
            messages.error(request, "Email already registered.")
            return redirect("Familyreg_page")

        if Registration.objects.filter(phn_no=phn_no).exists():
            messages.error(request, "Phone number already registered.")
            return redirect("Familyreg_page")

        try:
            Registration.objects.create(
                username=username,
                password=make_password(password),
                email_id=email_id,
                phn_no=phn_no,
                location=location,
                role="family",
                parent=parent_user
            )

            messages.success(request, "Family member registered successfully.")
            return redirect("Memberlist_page")

        except IntegrityError:
            messages.error(request, "User already exists.")
            return redirect("Familyreg_page")

    return redirect("Familyreg_page")


def Transaction1_page(request):
    logged_user = request.session.get("user_id")
    user = get_object_or_404(Registration,id=logged_user)
    transactions = Transaction.objects.filter(by=user)
    role =  request.session.get("role")
    return render(request, 'transaction_list1.html', {
        'transactions': transactions,
        'role':role})

def Transaction2_page(request):
    transactions = Transaction.objects.filter(owner_type='family')
    role =  request.session.get("role")
    return render(request, 'transaction_list2.html', {
        'transactions': transactions,
        'role':role})

def Categorylist_page(request):
    categories = Category.objects.all()
    role =  request.session.get("role")
    return render(request, 'category_list.html', {
        'categories': categories,
       'role':role})

def Memberlist_page(request):
    logged_user_id = request.session.get("user_id")

    members = Registration.objects.filter(
        role="family",
        parent_id=logged_user_id
    )

    role = request.session.get("role")

    return render(request, 'fam_member.html', {
        'members': members,
        'role': role
    })


def userlist_page(request):
    users = Registration.objects.filter(role='user')
    role =  request.session.get("role")
    return render(request, 'user_list.html', {
        'forms': users,
        'role':role})

# Edit and Delete functions

#1.Transaction
def trans1_delete(request, id):
    transac = Transaction.objects.get(id=id)
    transac.delete()
    return redirect('Transaction1_page')

def trans1_edit(request, id):
    transaction = Transaction.objects.get(id=id)

    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            form.save()
            return redirect('Transaction1_page')
    else:
        form = TransactionForm(instance=transaction)
    role =  request.session.get("role")
    return render(request, 'trans1_edit.html', {
        'forms': form,
        'role':role})

def trans2_edit(request, id):
    transaction = Transaction.objects.get(id=id)

    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transaction)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.owner_type = 'family'
            transaction.save()
            return redirect('Transaction2_page')
    else:
        form = TransactionForm(instance=transaction)
    role =  request.session.get("role")

    return render(request, 'trans2_edit.html', {
        'forms': form,
        'role':role
      })

def trans2_delete(request, id):
    Transaction.objects.filter(id=id).delete()
    return redirect('Transaction2_page')

#2.Family Member 

def member_delete(request, id):
    member = get_object_or_404(Registration, id=id)
    member.delete()
    return redirect('Memberlist_page')


def member_edit(request, id):
    member = get_object_or_404(Registration, id=id)
    if request.method == "POST":
        form = RegistrationForm(request.POST, instance=member)
        if form.is_valid():
            form.save()
            return redirect('Memberlist_page')
    else:
        form = RegistrationForm(instance=member)
        role =  request.session.get("role")
    return render(request, "member_edit.html", {
        'forms': form,
        'member': member,
        'role':role
        })

#3.User 
def user_delete(request, id):
    user = get_object_or_404(Registration, id=id)
    user.delete()
    return redirect('userlist_page')


def user_edit_page(request, id):
    user = get_object_or_404(Registration, id=id)
    if request.method == "POST":
        form = RegistrationForm(request.POST, instance=user)
        if form.is_valid():
            form.save()

            return redirect('userlist_page')
    else:
        form = RegistrationForm(instance=user)
    role =  request.session.get("role")
    return render(request, "user_edit.html", {
        'forms': form,
          'user': user,
          'role':role})

#4.Category

def category_delete(request, id):
    user = Category.objects.get(category_id=id)
    user.delete()
    return redirect('Categorylist_page')

def category_edit_page(request, id):
    cate = get_object_or_404(Category, id=id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=cate)
        if form.is_valid():
            form.save()
            return redirect('Categorylist_page')
    else:
        form = CategoryForm(instance=cate)
    role =  request.session.get("role")
    return render(request, "category_edit.html", {
        'forms': form, 
        'cate':cate,
        'role':role})

#5.Reminder of User

def remind1_delete(request, id):
    user = Reminder.objects.get(id=id)
    user.delete()
    return redirect('reminder_list1')

def remind2_delete(request, id):
    user = Reminder.objects.get(id=id)
    user.delete()
    return redirect('reminder_list2')

def remind1_edit_page(request, id):
    remind = get_object_or_404(Reminder, id=id)
    if request.method == "POST":
        form = ReminderForm(request.POST, instance=remind)
        if form.is_valid():
            form.save()
            return redirect('reminder_list1')
    else:
        form = ReminderForm(instance=remind)
    role =  request.session.get("role")
    return render(request, "remind1_edit.html", {
        'forms': form,
        'remind':remind,
        'role':role
        })

def remind2_edit_page(request, id):
    remind = get_object_or_404(Reminder, id=id)
    if request.method == "POST":
        form = ReminderForm(request.POST, instance=remind)
        if form.is_valid():
            form.save()
            return redirect('reminder_list2')
    else:
        form = ReminderForm(instance=remind)
    role =  request.session.get("role")
    return render(request, "remind2_edit.html", {
        'forms': form,
        'remind':remind,
        'role':role
        })

def user_reset_page(request):
    if request.method == "POST":
       form = RegistrationForm(request.POST)
       if form.is_valid():
           form.save()
       return HttpResponse("password_reseted")   
    return HttpResponse("Failed")

def user_category_page(request):
    if request.method == "POST":
        form = CategoryForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('Categorylist_page')
        else:
            print(form.errors)  
            return HttpResponse(f"Form errors: {form.errors}")
    form = CategoryForm()
    role =  request.session.get("role")
    return render(request, 'category.html', {
        'forms': form,
        'role':role,
        })

def user_expense_page(request):
    if request.method == "POST":
        logged_user = request.session.get('user_id')
        user = get_object_or_404(Registration,id=logged_user)
        form = TransactionForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.by = user
            obj.save()
            return redirect('Transaction1_page')
    role =  request.session.get("role")
    return render(request, 'expense.html', {
        'forms': TransactionForm(),
        'role':role
        })

def user_familyexpense_page(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        logged_user = request.session.get('user_id')
        user = get_object_or_404(Registration,id=logged_user)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.by = user
            obj.save()
            return redirect('Transaction2_page')
    role =  request.session.get("role")
    return render(request, 'familyexpense.html', {
        'forms': TransactionForm(),
        'role':role
        })


def user_reminder1_page(request):
    if request.method == "POST":
        form = ReminderForm(request.POST)

        if form.is_valid():
            # Get logged in user
            user_id = request.session.get("user_id")
            user = get_object_or_404(Registration, id=user_id)
            
            reminder = form.save(commit=False)
            reminder.owner_type = 'user'
            reminder.by = user  # Assign the user
            reminder.save()

            # ================= SEND EMAIL =================
            subject = "New Reminder Created"
            message = f"""
Hello,

Your reminder has been successfully created.

Date : {reminder.date}
Time : {reminder.time}
Description : {reminder.Reminder_desc}

Thank you for using Expense Tracker.
"""

            recipient_list = [reminder.Email_id]

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                fail_silently=False
            )

            return redirect('reminder_list1')
   #redirect after save



def user_reminder2_page(request):
    if request.method == "POST":
        form = ReminderForm(request.POST)

        if form.is_valid():
            # Get logged in user
            user_id = request.session.get("user_id")
            user = get_object_or_404(Registration, id=user_id)

            reminder = form.save(commit=False)
            reminder.owner_type = 'family'
            reminder.by = user # Assign the user
            reminder.save()

            subject = "Family Reminder Created"
            message = f"""
Hello,

A new family reminder has been created.

Date : {reminder.date}
Time : {reminder.time}
Description : {reminder.Reminder_desc}
"""

            send_mail(
                subject,
                message,
                settings.DEFAULT_FROM_EMAIL,
                [reminder.Email_id],
                fail_silently=False
            )

            return redirect('reminder_list2')
# redirect after save


#phonepe functions
def paypage(request):
    return render(request, 'payment.html')

def payment_send(request):
    unique_order_id = str(uuid4())  #your merchentorderid
    amount_paisa = request.POST.get('amount')
    amount_rupees = int(amount_paisa) *100
    client = get_phonepe_client()#intiated client
    meta_info = meta_info_generation()
    redirect_url = request.build_absolute_uri(
        reverse("payment_confo") #make sure you have this url/view
    )

    payrequest = buil_request(client,unique_order_id,amount_rupees,redirect_url,meta_info)
    standard_pay_response = client.pay(payrequest)
    request.session["last_order_id"] = unique_order_id
    checkout_page_url = standard_pay_response.redirect_url
    return redirect(checkout_page_url)

def payment_confo(request):
    #get the last order id from session
    merchent_order_id = request.session.get("last_order_id")
    if not merchent_order_id:
        return HttpResponse("no order ID found in session", status=400)
    
    client = get_phonepe_client()
    #depending on SDK version this might be get_order_status or check_status
    status = client.get_order_status(merchent_order_id)

    return HttpResponse(
        f"Return from PhonePe,<br>"
        f"Order: {merchent_order_id}<br>"
        f"Status: {status.state}<br>"
        f"Amount: {status.amount/100}<br>"
    )


#Email functions

def email_otp(request):
    return render(request, 'email_OTP.html')

def user_email_page(request):
    if request.method == "POST":
        form = RegistrationForm(request.POST)
        email = request.POST.get('email_id')
        print(email)

        try:
            user= Registration.objects.get(email_id=email)
            request.session['email_id'] = user.email_id
            subject= "Expence tracker password reset"
            otp = random.randint(1000,9999)
            body = f"otp for your password reset = {otp}"
            send = send_email(email,subject,body)
            request.session['otp'] = otp
            return render(request, 'verify_otp.html')
        except Registration.DoesNotExist: 
            return HttpResponse("no user in this email id")  


# -- Reports view


def reports_page(request):

    user_id = request.session.get('user_id')
    if not user_id:
        return redirect("login_page")

    user = get_object_or_404(Registration, id=user_id)
    role = user.role

    mode = request.GET.get("mode", "individual")

    # ------------------ MODE LOGIC ------------------

    if mode == "family" and role == "user":

    # Get family members
        members = Registration.objects.filter(parent=user)

    # Create list of user IDs (members + main user)
        user_ids = list(members.values_list("id", flat=True))
        user_ids.append(user.id)

    # Get transactions of both
        transactions = Transaction.objects.filter(by__in=user_ids)

    else:
        # My report (only logged user)
        transactions = Transaction.objects.filter(by=user)

    # ------------------ DATE FILTER ------------------

    range_type = request.GET.get("range")
    start = request.GET.get("start")
    end = request.GET.get("end")

    if range_type == "this_month":
        today = datetime.today().date()
        start_date = today.replace(day=1)
        transactions = transactions.filter(date__gte=start_date)

    elif range_type == "last_6_months":
        start_date = (datetime.today() - timedelta(days=180)).date()
        transactions = transactions.filter(date__gte=start_date)

    elif start and end:
        start_date = datetime.strptime(start, "%Y-%m-%d").date()
        end_date = datetime.strptime(end, "%Y-%m-%d").date()
        transactions = transactions.filter(date__range=[start_date, end_date])

    # ------------------ SUMMARY ------------------

    income_total = transactions.filter(Type__iexact="income").aggregate(
        total=Sum("amount")
    )["total"] or 0

    expense_total = transactions.filter(Type__iexact="expense").aggregate(
        total=Sum("amount")
    )["total"] or 0

    balance = income_total - expense_total

    # ------------------ MONTHLY CHART ------------------

    monthly = (
        transactions
        .annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(
            income=Sum("amount", filter=Q(Type__iexact="income")),
            expense=Sum("amount", filter=Q(Type__iexact="expense"))
        )
        .order_by("month")
    )

    months = []
    income_data = []
    expense_data = []

    for row in monthly:
        if row["month"]:
            months.append(row["month"].strftime("%b %Y"))
            income_data.append(row["income"] or 0)
            expense_data.append(row["expense"] or 0)

    # ------------------ CATEGORY PIE ------------------

    category_data = (
        transactions
        .filter(Type__iexact="expense")
        .values("category_id__category_type")
        .annotate(total=Sum("amount"))
    )

    category_labels = [c["category_id__category_type"] for c in category_data]
    category_values = [c["total"] for c in category_data]

    return render(request, "reports.html", {
        "role": role,
        "mode": mode,
        "income": income_total,
        "expense": expense_total,
        "balance": balance,
        "transactions": transactions,

        "months_json": json.dumps(months),
        "income_json": json.dumps(income_data),
        "expense_json": json.dumps(expense_data),
        "category_labels_json": json.dumps(category_labels),
        "category_values_json": json.dumps(category_values),
    })


def generate_pdf(request):

    user_id = request.session.get("user_id")
    if not user_id:
        return redirect("login_page")

    user = get_object_or_404(Registration, id=user_id)

    # ----------- INDIVIDUAL TRANSACTIONS -----------
    individual_transactions = Transaction.objects.filter(by=user)

    individual_income = individual_transactions.filter(
        Type__iexact="income"
    ).aggregate(total=Sum("amount"))["total"] or 0

    individual_expense = individual_transactions.filter(
        Type__iexact="expense"
    ).aggregate(total=Sum("amount"))["total"] or 0

    individual_balance = individual_income - individual_expense

    # ----------- FAMILY TRANSACTIONS -----------
    members = Registration.objects.filter(parent=user)

    family_transactions = Transaction.objects.filter(
        Q(by=user) | Q(by__in=members)
    )

    family_income = family_transactions.filter(
        Type__iexact="income"
    ).aggregate(total=Sum("amount"))["total"] or 0

    family_expense = family_transactions.filter(
        Type__iexact="expense"
    ).aggregate(total=Sum("amount"))["total"] or 0

    family_balance = family_income - family_expense

    # ----------- RENDER PDF -----------
    template = get_template("report_pdf.html")
    html = template.render({
        "individual_transactions": individual_transactions,
        "individual_income": individual_income,
        "individual_expense": individual_expense,
        "individual_balance": individual_balance,

        "family_transactions": family_transactions,
        "family_income": family_income,
        "family_expense": family_expense,
        "family_balance": family_balance,
    })

    response = HttpResponse(content_type="application/pdf")
    response["Content-Disposition"] = "attachment; filename=expense_report.pdf"

    pisa.CreatePDF(html, dest=response)

    return response


def forgot_password(request):
    if request.method == "POST":
        email = request.POST.get('email', '').strip().lower()
        print("EMAIL ENTERED:", email)
        user = Registration.objects.filter(email_id__iexact=email).first()
        print("USER FOUND:", user)
        if user:
            otp = str(random.randint(100000, 999999))
            user.otp = otp
            user.save()
            print("OTP GENERATED:", otp)
            send_mail(
                'Password Reset OTP',
                f'Your OTP is: {otp}',
                'your_email@gmail.com',
                [email],
                fail_silently=False,
            )
            request.session['reset_user'] = user.id
            messages.success(request, "OTP sent to your email.")
            return redirect('verify_otp')
        else:
            messages.error(request, "Email not registered.")
    role =  request.session.get("role")
    return render(request, 'forgot_password.html',{'role':role})


def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        user_id = request.session.get('reset_user')
        user = Registration.objects.get(id=user_id)

        if user.otp == entered_otp:
            return redirect('reset_password')
        else:
            messages.error(request, "Invalid OTP")
    role =  request.session.get("role")
    return render(request, 'verify_otp.html',{'role':role})

def reset_password(request):
    user_id = request.session.get('reset_user')
    user = Registration.objects.get(id=user_id)

    if request.method == "POST":
        p1 = request.POST.get('password')
        p2 = request.POST.get('confirm_password')

        if p1 != p2:
            messages.error(request, "Passwords do not match")
        else:
            user.password = make_password(p1)
            user.confirm_password = make_password(p1)
            user.otp = None
            user.save()
            messages.success(request, "Password reset successful")
            return redirect('login_page')
    role =  request.session.get("role")
    return render(request, 'reset_password.html',{'role':role})

#end of view functions