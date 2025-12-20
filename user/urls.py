from django.urls import path  # type: ignore
from . import views


urlpatterns = [
    #render
     path('user/login', views.login_page, name='login_page'),
     path('user/register',views.Register_page, name='Register_page'),
     path('user/expense',views.Expense_page, name='Expense_page'),
     path('user/dashboard1',views.Dashboard1_page, name='Dashboard1_page'),
     path('user/dashboard2',views.Dashboard2_page, name='Dashboard2_page'),
     path('user/reset',views.Reset_page, name='Reset_page'),
     path('user/familyexpense',views.Familyexpense_page, name='Familyexpense_page'),
     path('user/category',views.Category_page, name='Category_page'),
     path('user/Family',views.Familyreg_page, name='Familyreg_page'),
     path('user/UserHome_page',views.UserHome_page, name='UserHome_page'),
     path('user/FamHome_page',views.FamHome_page, name='FamHome_page'),
     path('user/reminder1',views.Reminder1_page, name='Reminder1_page'),
     path('user/reminder2',views.Reminder2_page, name='Reminder2_page'),
     path('user/main_home',views.main_home, name='main_home'),

    #List urls
     path('user/Transaction1',views.Transaction1_page, name='Transaction1_page'),
     path('user/Transaction2',views.Transaction2_page, name='Transaction2_page'),
     path('user/categorylist',views.Categorylist_page, name='Categorylist_page'),
     path('user/reminderlist1',views. reminder_list1, name='reminder_list1'),
     path('user/reminderlist2',views. reminder_list2, name='reminder_list2'),
     path('user/memberlist',views.Memberlist_page , name='Memberlist_page'),
     path('user/userlist',views.userlist_page , name='userlist_page'),
     
     #Email and payment urls
     path('user/pay',views.paypage, name='paypage'),
     path('user/payment_send',views.payment_send, name='payment_send'),
     path('user/payment_confo',views.payment_confo, name='payment_confo'),
     path('user/email',views.email_otp, name='email_otp'),
     

     #Edit and Delete functions urls
     path('user/member_delete/<int:id>/',views.member_delete,name='member_delete'),
     path('user/member_edit/<int:id>/',views.member_edit,name='member_edit'),
     path('user/user_delete/<int:id>/',views.user_delete,name='user_delete'),
     path('user/user_edit/<int:id>/',views.user_edit_page,name='user_edit_page'),
     path('user/category_delete/<int:id>/',views.category_delete,name='category_delete'),
     path('user/category_edit/<int:id>/',views.category_edit_page,name='category_edit_page'),
     path('user/remind1_delete/<int:id>/',views.remind1_delete,name='remind1_delete'),
     path('user/remind1_edit/<int:id>/',views.remind1_edit_page,name='remind1_edit_page'),
     path('user/trans1_delete/<int:id>/',views.trans1_delete,name='trans1_delete'),
     path('user/trans1_edit/<int:id>/',views.trans1_edit,name='trans1_edit'),


   #action
     path('user/user_reg1_action',views.user_reg1_page, name='user_reg1_page'),
     path('user/user_reg2_action',views.user_reg2_page, name='user_reg2_page'),
     path('user/user_reset_action',views.user_reset_page, name='user_reset_page'),
     path('user/user_login_action',views.user_login_page, name='user_login_page'),
     path('user/user_category_action',views.user_category_page, name='user_category_page'),
     path('user/user_expense_action',views.user_expense_page, name='user_expense_page'),
     path('user/user_familyexpense_action',views.user_familyexpense_page, name='user_familyexpense_page'),
     path('user/user_reminder_action1',views.user_reminder1_page, name='user_reminder1_page'),
     path('user/user_reminder_action2',views.user_reminder2_page, name='user_reminder2_page'),
     path('user/user_email_action',views.user_email_page, name='user_email_page'),
  
]