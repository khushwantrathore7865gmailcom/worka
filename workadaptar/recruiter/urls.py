from django.urls import include, path, reverse_lazy
from .views import SignUpView, ActivateAccount, Home, login_employer, edit_job, delete_job, job_detail, publish_job, \
    view_applied_candidate, disqualify, shortlist, job_post, shortlistview_applied_candidate, \
    disqualifyview_applied_candidate,ProfileView,unpublish,remove_unpublish,advance_Search
from . import views
from django.contrib.auth import views as auth_views  # import this

app_name = 'recruiter'
urlpatterns = [
    path('', Home, name='employer_home'),
    path('addjob/', job_post, name='job_post'),
    path('editjob/<int:pk>', edit_job, name='edit_job'),
    path('deletejob/<int:pk>', delete_job, name='delete_job'),
    path('jobdetail/<int:pk>', job_detail, name='job_detail'),
    path('jobdetail/publishjob/<int:pk>', publish_job, name='publish_job'),
    path('jobdetail/applied_candidate/<int:pk>', view_applied_candidate, name='view_applied_candidate'),
    path('jobdetail/applied_candidate/shortlistview/<int:pk>', shortlistview_applied_candidate,
         name='shortlist_view_applied_candidate'),
    path('jobdetail/applied_candidate/disqualifyview/<int:pk>', disqualifyview_applied_candidate,
         name='disqualify_view_applied_candidate'),
    path('jobdetail/applied_candidate/shortlist/<int:pk>', shortlist, name='shortlist'),
    path('jobdetail/applied_candidate/disqualify/<int:pk>', disqualify, name='disqualify'),
    path('unpublish/<int:pk>', unpublish, name='unpublish'),
    path('removeunpublish/<int:pk>', remove_unpublish, name='remove_unpublish'),
    path('viewprofile/', ProfileView, name='profile'),
    path('login', login_employer, name='employer/login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='/'), name='logout'),
    path('signup', SignUpView.as_view(), name='employer/register'),
    path('reset_password/', auth_views.PasswordResetView.as_view(
        template_name='account/password_reset.html', email_template_name='account/password_reset_email.html',success_url = reverse_lazy('recruiter:password_reset_done')),
         name='reset_password'),
    path('reset_password_sent/', auth_views.PasswordResetDoneView.as_view(
        template_name='account/password_reset_done.html'), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(
        template_name="account/password_reset_confirm.html"), name='password_reset_confirm'),
    path('account/reset_password_complete/', auth_views.PasswordResetCompleteView.as_view(
        template_name='account/password_reset_complete.html'), name='password_reset_complete'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),
    path('advance-search/',advance_Search,name='advance-search')
]