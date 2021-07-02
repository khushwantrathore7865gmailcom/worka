from django.urls import include, path
from jobseeker.views import SignUpView, ActivateAccount, jobseeker_Home
from . import views
from django.contrib.auth import views as auth_views  # import this

urlpatterns = [
    path('', jobseeker_Home, name='jobseeker_home'),
    path('login', views.login_candidate, name='jobseeker/login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='jobseeker/login'), name='logout'),
    path('signup', SignUpView.as_view(), name='jobseeker/register'),

    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='account/password_reset.html'), name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="account/password_reset_confirm.html"), name='password_reset_confirm'),
    path('account/reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password_reset_complete.html'), name='password_reset_complete'),

    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),

]
