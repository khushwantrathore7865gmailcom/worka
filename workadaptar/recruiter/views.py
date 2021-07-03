from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from user_custom.models import User_custom
from django.utils.encoding import force_text
from .models import Employer, Employer_profile, Employer_candidate_jobanswer, Employer_job, Employer_job_Applied
from .forms import SignUpForm, ProfileRegisterForm, JobPostForm, JobsQuestionForm
from django.views.generic import View
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from .tokens import account_activation_token


class SignUpView(View):
    form_class = SignUpForm

    template_name = 'employer/signup.html'

    def get(self, request, *args, **kwargs):
        form = self.form_class()
        print(User_custom.objects.all())
        return render(request, self.template_name, {'form': form})

    def post(self, request, *args, **kwargs):
        form = self.form_class(request.POST)

        if form.is_valid():
            emaill = form.cleaned_data['email']
            if User_custom.objects.filter(email=emaill).exists():

                return HttpResponse('User with same email already exists, Please try again with different Username!!')
            else:
                user = form.save(commit=False)
                user.username = user.email
                user.is_active = True  # change this to False after testing
                user.is_employeer = True
                user.save()
                new_employe = Employer(user=user, is_email_verified=False)
                new_employe.save()
                current_site = get_current_site(request)
                subject = 'Activate Your WorkAdaptar Account'
                message = render_to_string('emails/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(new_employe),
                })
                # user.email_user(subject, message)
                messages.success(
                    request, ('Please check your mail for complete registration.'))
                # return redirect('login')
                return render(request, self.template_name, {'form': form})
        else:
            return render(request, self.template_name, {'form': form})


class ActivateAccount(View):

    def get(self, request, uidb64, token, *args, **kwargs):
        try:
            uid = force_text(urlsafe_base64_decode(uidb64))
            user = User_custom.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError, User_custom.DoesNotExist):
            user = None

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True

            pr = Employer.objects.get(user=user)
            pr.is_email_verified = True
            pr.save()
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('dashboard_home')
        else:
            messages.warning(
                request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('dashboard_home')

def login_employer(request):

    if request.user.is_authenticated and request.user.is_employeer:
        print(request.user)
        return redirect('employer_home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('pass')
            print(username)
            print(password)
            user = authenticate(request, username=username, password=password)
            print(user)
            if user is not None and user.is_employeer:
                login(request, user)
                return redirect('employer_home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'employer/login.html', context)

def Home(request):
    c = Employer.objects.get(user=request.user)
    if Employer_profile.objects.get(employer=c):
        job = Employer_job.objects.filter(employer_id = c)
        context = {'jobs':job}
        return render(request, 'employer/job-post.html', context)
    else:
        return redirect('')


# @login_required(login_url='/login/')
def ProfileView(request, pk):
    profile = Employer.objects.get(user=User_custom.objects.get(id=pk))
    if request.method == 'POST':
        form1 = ProfileRegisterForm(request.POST)
        if form1.is_valid():
            f1 = form1.save(commit=False)
            f1.user_id = profile
        #
    form1 = ProfileRegisterForm()

    return render(request, 'dashboard/my-profile.html', {"form1": form1})


def job_post(request):
    e = Employer.objects.get(user=request.user)
    if request.method == 'POST':
        form1 = JobPostForm(request.POST)
        if form1.is_valid():
            f1 = form1.save(commit=False)
            f1.employer_id = e

            form2 = JobsQuestionForm(request.POST)
            if form2.is_valid():
                f2 = form2.save(commit=False)
                f2.employer_id = e
                f2.job_id = f1
                f2.save()
                f1.save()
    form1 = JobPostForm(request.POST)
    form2 = JobsQuestionForm(request.POST)
    return render(request, 'dashboard/addjob.html', {"form1": form1, "form2": form2})


def job_Response(request, pk):
    job = Employer_job.objects.get(pk=pk)
    response = Employer_job_Applied.objects.filter(job_id=job)
    return render(request, 'dashboard/jobresponse.html', {'response': response})

