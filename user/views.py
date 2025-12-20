from django.http import HttpResponse # type: ignore
from django .shortcuts import render,redirect,get_object_or_404 # type: ignore
from .models import Registration, Notification, Transaction, Category, Reminder
from .forms import LoginForm, RegistrationForm,TransactionForm,DashboardForm,ResetForm,CategoryForm,ReminderForm
from .util import get_phonepe_client,meta_info_generation,buil_request
from django.urls import reverse
from uuid import uuid4
from .util import send_email
import random

# Create your views here.
def main_home(request):
    return render(request, 'home.html')

def login_page(request):
    register=LoginForm
    return render(request, 'login.html', {'forms':register})


def Register_page(request):
    Register=RegistrationForm()
    return render(request, 'registration.html',{'forms':Register})

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

def UserHome_page(request):
    return render(request, 'userhome.html')

def FamHome_page(request):
    return render(request, 'famhome.html')

def Reminder1_page(request):
    reminder1 = ReminderForm()
    return render(request, 'reminder1.html', {'forms':reminder1})

def Reminder2_page(request):
    reminder2 = ReminderForm()
    return render(request, 'reminder2.html', {'forms':reminder2})

#List functions

def reminder_list1(request):
    remind = Reminder.objects.all()
    return render(request, 'reminder_list1.html', {'forms':remind})

def reminder_list2(request):
    remind2 = Reminder.objects.all()
    return render(request, 'reminder_list2.html',{'forms':remind2})

def Transaction1_page(request):
    Trans = Transaction.objects.all()
    return render(request, 'transaction_list1.html', {'forms':Trans})

def Transaction2_page(request):
    trans = Transaction.objects.all()
    return render(request, 'transaction_list2.html', {'forms':trans})

def Categorylist_page(request):
    category1= Category.objects.all()
    return render(request, 'category_list.html', {'forms':category1})

def Memberlist_page(request):
    memb = Registration.objects.filter(usertype='family_member')
    return render(request, 'fam_member.html', {'forms':memb})

def userlist_page(request):
    users = Registration.objects.filter(usertype='user')
    return render(request, 'user_list.html', {'forms':users})


# Edit and Delete functions

#1.Transaction
def trans1_delete(request, id):
    transac = Transaction.objects.get(id=id)
    transac.delete()
    return redirect('Transaction1_page')

def trans1_edit(request, id):
    transac = get_object_or_404(Transaction, id=id)
    if request.method == "POST":
        form = TransactionForm(request.POST, instance=transac)
        if form.is_valid():
            form.save()
            return redirect('Transaction1_page')
    else:
        form = TransactionForm(instance=transac)
    return render(request, "trans1_edit.html", {'forms': form, 'transac': transac})

#2.Family Member 


def member_delete(request, id):
    member = Registration.objects.get(Registration_id=id)
    member.delete()
    return redirect('Memberlist_page')


def member_edit(request, id):
    member = get_object_or_404(Registration, Registration_id=id)
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
    user = Registration.objects.get(Registration_id=id)
    user.delete()
    return redirect('userlist_page')

def user_edit_page(request, id):
    user = get_object_or_404(Registration, Registration_id=id)
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





#Action Page Functions
     


def user_reg1_page(request):
    if request.method == "POST":
       form = RegistrationForm(request.POST)
       if form.is_valid():
           obj1 = form.save(commit=False)
           obj1.usertype = "user"
           obj1.save()
       return redirect('login_page')
     

def user_reg2_page(request): 
        if request.method == "POST":
           form = RegistrationForm(request.POST)
           if form.is_valid():
               obj2 = form.save(commit=False)
               obj2.usertype = "family_member"
               obj2.save()
        return HttpResponse("Family Member Added")


def user_login_page(request):
    if request.method == "POST":
            username= request.POST.get('username')
            password= request.POST.get('password')

    try:
            user= Registration.objects.get(username=username, password=password)
            request.session['username'] = user.username
            request.session['password'] = user.password
            if user.usertype == 'user':
                return redirect('UserHome_page')
            else:
                return redirect('FamHome_page')

    except Registration.DoesNotExist: 
            return HttpResponse("login not sucsesfull.Invalid username or password")   
 

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
             
    return HttpResponse("Failed")


def user_expense_page(request):
    if request.method == "POST":
       form = TransactionForm(request.POST)
       if form.is_valid():
          form.save()
       return redirect('Transaction1_page')
    


def user_familyexpense_page(request):
    if request.method == "POST":
          form = TransactionForm(request.POST)
          if form.is_valid():
             form.save()
          return redirect('Transaction2_page')



def user_reminder1_page(request):
    if request.method == "POST":
       form = ReminderForm(request.POST)
       if form.is_valid():
           form.save()
           
       return redirect('reminder_list1')   
    
    return HttpResponse("Failed")


def user_reminder2_page(request):
    if request.method == "POST":
       form = ReminderForm(request.POST)
       if form.is_valid():
           form.save()
           
       return redirect('reminder_list2')   
    
    return HttpResponse("Failed")


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

            
