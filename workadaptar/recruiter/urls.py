from django.urls import include, path
from .views import SignUpView, ActivateAccount,Home,login_employer
from . import views
from django.contrib.auth import views as auth_views  # import this
urlpatterns = [
    path('', Home, name='employer_home'),
    path('login', login_employer, name='employer/login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='employer/login'), name='logout'),
    path('signup', SignUpView.as_view(), name='employer/register'),
    path('activate/<uidb64>/<token>/', ActivateAccount.as_view(), name='activate'),


]