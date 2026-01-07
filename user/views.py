from django.http import HttpResponse # type: ignore
from django .shortcuts import render,redirect,get_object_or_404 # type: ignore
from .models import Registration, Notification, Transaction, Category, Reminder
from .forms import LoginForm, RegistrationForm,TransactionForm,DashboardForm,ResetForm,CategoryForm,ReminderForm
# from .util import get_phonepe_client,meta_info_generation,buil_request
from django.urls import reverse
from uuid import uuid4
# from .util import send_email
from django.core.mail import send_mail
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
print("DATETIME IMPORT CHECK:", datetime)
from django.conf import settings


#BASIC Page Renders

def main_home(request):
    return render(request, 'home.html')

def login_page(request):
    register=LoginForm
    return render(request, 'login.html', {'forms':register})

def Register_page(request):
    Register=RegistrationForm()
    return render(request, 'registration.html',{'forms':Register})

def UserHome_page(request):
    return render(request, 'userhome.html')

def FamHome_page(request):
    return render(request, 'famhome.html')

def Expense_page(request):
    Expense=TransactionForm()
    return render(request, 'expense.html', {'forms':Expense})

def Dashboard1_page(request):
    Dashboard1=DashboardForm()
    return render(request, 'dashboard1.html', {'forms':Dashboard1})

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
    return render(request, 'category.html', {'forms':category})


def Familyreg_page(request):
    familyregister=RegistrationForm()
    return render(request, 'familyreg.html',{'forms':familyregister})

def Reminder1_page(request):
    reminder1 = ReminderForm()
    return render(request, 'reminder1.html', {'forms':reminder1})

def Reminder2_page(request):
    reminder2 = ReminderForm()
    return render(request, 'reminder2.html', {'forms':reminder2})

def reminder_list1(request):
    reminders = Reminder.objects.filter(owner_type='user')
    return render(request, 'reminder_list1.html', {'reminders': reminders})

def reminder_list2(request):
    reminders = Reminder.objects.filter(owner_type='family')
    return render(request, 'reminder_list2.html', {'reminders': reminders})


# Login Action Page

def user_login_page(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = Registration.objects.filter(username=username, password=password).first()
        if not user:
            return HttpResponse("Login failed. Invalid username or password")
        request.session["username"] = user.username
        request.session["user_id"] = user.id
        if user.role == "user":
            return redirect("UserHome_page")
        else:
            return redirect("FamHome_page")
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
            return HttpResponse("Passwords do not match")

        Registration.objects.create(
            username=username,
            password=password,
            confirm_password=confirm_password,
            email_id=email_id,
            phn_no=phn_no,
            location=location,
            role="user"   # user
        )

        return redirect("user_login_page")

    return render(request, "user/user_register.html")

#family member Registration Action Pages

def user_reg2_page(request):

    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        confirm_password = request.POST.get("confirm_password")
        email_id = request.POST.get("email_id")
        phn_no = request.POST.get("phn_no")
        location = request.POST.get("location")

        if password != confirm_password:
            messages.error(request, "Passwords do not match.")
        else:
            try:
                Registration.objects.create(
                    username=username,
                    password=password,
                    confirm_password=confirm_password,
                    email_id=email_id,
                    phn_no=phn_no,
                    location=location,
                    role="family"
                )
                messages.success(request, "Family member registered successfully.")
            except:
                messages.error(request, "Error in registering family member.")

    return render(request, "famhome.html")

#transaction, category, member, user list pages

def Transaction1_page(request):
    transactions = Transaction.objects.filter(owner_type='user')
    return render(request, 'transaction_list1.html', {'transactions': transactions})

def Transaction2_page(request):
    transactions = Transaction.objects.filter(owner_type='family')
    return render(request, 'transaction_list2.html', {'transactions': transactions})

def Categorylist_page(request):
    categories = Category.objects.all()
    return render(request, 'category_list.html', {'categories': categories})

def Memberlist_page(request):
    members = Registration.objects.filter(role='family')
    return render(request, 'fam_member.html', {'members': members})

def userlist_page(request):
    users = Registration.objects.filter(role='user')
    return render(request, 'user_list.html', {'forms': users})

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

    return render(request, 'trans1_edit.html', {'forms': form})

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

    return render(request, 'trans2_edit.html', {'forms': form})

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
    return render(request, "member_edit.html", {'forms': form, 'member': member})

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
    return render(request, "user_edit.html", {'forms': form, 'user': user})

#4.Category

def category_delete(request, id):
    user = Category.objects.get(category_id=id)
    user.delete()
    return redirect('Categorylist_page')

def category_edit_page(request, id):
    cate = get_object_or_404(Category, category_id=id)
    if request.method == "POST":
        form = CategoryForm(request.POST, instance=cate)
        if form.is_valid():
            form.save()
            return redirect('Categorylist_page')
    else:
        form = CategoryForm(instance=cate)
    return render(request, "category_edit.html", {'forms': form, 'cate':cate})

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
    return render(request, "remind1_edit.html", {'forms': form, 'remind':remind})

def remind2_edit_page(request, id):
    remind = get_object_or_404(Reminder, id=id)
    if request.method == "POST":
        form = ReminderForm(request.POST, instance=remind)
        if form.is_valid():
            form.save()
            return redirect('reminder_list2')
    else:
        form = ReminderForm(instance=remind)
    return render(request, "remind2_edit.html", {'forms': form, 'remind':remind})

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
    return render(request, 'category.html', {'forms': form})

def user_expense_page(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner_type = 'user'
            obj.save()
            return redirect('Transaction1_page')

    return render(request, 'expense.html', {'forms': TransactionForm()})

def user_familyexpense_page(request):
    if request.method == "POST":
        form = TransactionForm(request.POST)
        if form.is_valid():
            obj = form.save(commit=False)
            obj.owner_type = 'family'
            obj.save()
            return redirect('Transaction2_page')

    return render(request, 'familyexpense.html', {'forms': TransactionForm()})


def user_reminder1_page(request):
    if request.method == "POST":
        form = ReminderForm(request.POST)

        if form.is_valid():
            reminder = form.save(commit=False)
            reminder.owner_type = 'user'
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
            reminder = form.save(commit=False)
            reminder.owner_type = 'family'
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

    transactions = Transaction.objects.all()

    range_type = request.GET.get("range")
    start = request.GET.get("start")
    end = request.GET.get("end")

    # ------------------ APPLY FILTERS ------------------

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

    income_total = transactions.filter(Type__icontains="income").aggregate(total=Sum("amount"))["total"] or 0
    expense_total = transactions.filter(Type__icontains="expense").aggregate(total=Sum("amount"))["total"] or 0
    balance = income_total - expense_total

    # ------------------ MONTHLY CHART ------------------

    monthly = (
        transactions
        .annotate(month=TruncMonth("date"))
        .values("month")
        .annotate(
            income=Sum("amount", filter=Q(Type__icontains="income")),
            expense=Sum("amount", filter=Q(Type__icontains="expense"))
        )
        .order_by("month")
    )

    months = []
    income_data = []
    expense_data = []

    for row in monthly:
        if row["month"] is not None:
            months.append(row["month"].strftime("%b %Y"))
            income_data.append(row["income"] or 0)
            expense_data.append(row["expense"] or 0)

    # ------------------ CATEGORY PIE ------------------

    category_data = (
        transactions
        .filter(Type__icontains="expense")
        .values("category_id__category_type")
        .annotate(total=Sum("amount"))
    )

    category_labels = [c["category_id__category_type"] for c in category_data]
    category_values = [c["total"] for c in category_data]

    # ------------------ RENDER ------------------

    return render(request, "reports.html", {
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
    transactions = Transaction.objects.all()
    income = transactions.filter(Type__iexact='income').aggregate(total=Sum('amount'))['total'] or 0
    expense = transactions.filter(Type__iexact='expense').aggregate(total=Sum('amount'))['total'] or 0

    balance = income - expense

    template = get_template("report_pdf.html")
    html = template.render({
        'transactions': transactions,
        'income': income,
        'expense': expense,
        'balance': balance,
    })

    response = HttpResponse(content_type='application/pdf')
    response['Content-Disposition'] = 'attachment; filename="expense_report.pdf"'
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
    return render(request, 'forgot_password.html')


def verify_otp(request):
    if request.method == "POST":
        entered_otp = request.POST.get('otp')
        user_id = request.session.get('reset_user')
        user = Registration.objects.get(id=user_id)

        if user.otp == entered_otp:
            return redirect('reset_password')
        else:
            messages.error(request, "Invalid OTP")

    return render(request, 'verify_otp.html')

def reset_password(request):
    user_id = request.session.get('reset_user')
    user = Registration.objects.get(id=user_id)

    if request.method == "POST":
        p1 = request.POST.get('password')
        p2 = request.POST.get('confirm_password')

        if p1 != p2:
            messages.error(request, "Passwords do not match")
        else:
            user.password = p1
            user.confirm_password = p1
            user.otp = None
            user.save()
            messages.success(request, "Password reset successful")
            return redirect('login_page')

    return render(request, 'reset_password.html')

#end of view functions