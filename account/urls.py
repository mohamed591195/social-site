from django.urls import path
from django.contrib.auth import views as auth_views
from . import views
from django.urls import reverse_lazy

app_name = 'account'
urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='account/login.html'), name='login_page'),
    path('logout/', auth_views.LogoutView.as_view(template_name='account/logout.html'), name='logout_page'),
    path('register/', views.RegisterView, name='register_page'),
    path('', views.dash, name='dash_page'),


    path('password_change/', 
    auth_views.PasswordChangeView.as_view(
        template_name='account/passchange.html', 
        success_url=reverse_lazy('account:pass_change_done')
        )
        ,name='pass_change_page'),


    path('password_change_done/', 
    auth_views.PasswordChangeDoneView.as_view(
        template_name='account/passchangedone.html'
        ),
         name='pass_change_done'),


    path('password_reset/', 
    auth_views.PasswordResetView.as_view(
        template_name='account/passreset.html', 
        email_template_name='account/passreset_email.html', 
        success_url=reverse_lazy('account:pass_reset_done_page')
        ), 
        name='pass_reset_page'),


    path('password_reset_done', 
    auth_views.PasswordResetDoneView.as_view(
        template_name='account/passreset_done.html'
        ),
         name='pass_reset_done_page'),


    path('password_reset_confirm/<uidb64>/<token>/',
     auth_views.PasswordResetConfirmView.as_view(
         template_name='account/passreset_confirm.html',
         success_url=reverse_lazy('account:pass_reset_complete') 
         ), 
         name='pass_confirm_page'),
    
    path('password_reset_complete', 
    auth_views.PasswordResetCompleteView.as_view(
        template_name='account/passreset_complete.html'
        ),
        name='pass_reset_complete'),
    
    path('edit/', views.EditView, name='editinfo_page'),
    path('users/', views.user_list, name='user_list'),
    path('users/<username>/', views.user_detail, name='user_detail'),
    path('follow/', views.follow_user, name='follow_link')


    

]
