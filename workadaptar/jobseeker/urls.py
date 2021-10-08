from django.urls import include, path, reverse_lazy
from .views import SignUpView, ActivateAccount, jobseeker_Home, ProfileView, save_later, SavedJobs, AppliedJobs, \
    remove_applied, remove_saved, ProfileEdit, ResumeCreation,payment,create_profile,sendVerificationMail
from . import views
from django.contrib.auth import views as auth_views  # import this

app_name = 'jobseeker'
urlpatterns = [
    path('', jobseeker_Home, name='jobseeker_home'),
    path('savedJobs/', SavedJobs, name='SavedJobs'),
    path('appliedJobs/', AppliedJobs, name='AppliedJobs'),
    path('removeApplied/<int:pk>', remove_applied, name='remove'),
    path('removeSaved/<int:pk>', remove_saved, name='remove_saved'),
    path('save/<int:pk>', save_later, name='save_job'),
    path('login', views.login_candidate, name='jobseeker/login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('signup', SignUpView.as_view(), name='jobseeker/register'),

    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='account/password_reset.html', email_template_name='account/password_reset_email.html',success_url = reverse_lazy('jobseeker:password_reset_done')),
         name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="account/password_reset_confirm.html",success_url=reverse_lazy('jobseeker:password_reset_complete')), name='password_reset_confirm'),
    path('account/reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password_reset_complete.html'), name='password_reset_complete'),
    path('viewprofile/', ProfileView, name='profile'),
    path('profile_edit/', ProfileEdit, name='ProfileEdit'),
    path('create_profile/', ProfileEdit, name='create_profile'),
    # path('create_profile/',create_profile, name='create_profile'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('send_verification_mail',sendVerificationMail,name='sendVerificationMail'),
    path('resume/', ResumeCreation, name='resume'),
    path('resume_payment/<Experience>/<int:add>/', payment, name='resume_payment'),
]