from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from user_custom.models import User_custom
from django.utils.encoding import force_text
from .models import Candidate, Candidate_profile, Candidate_edu, Candidate_skills, Candidate_profdetail, \
    Candidate_resume
from jobseeker.forms import SignUpForm, ProfileRegisterForm, ProfileRegisterForm_edu, ProfileRegisterForm_profdetail, \
    ProfileRegisterForm_resume
from django.views.generic import View
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect
from jobseeker.tokens import account_activation_token
from recruiter.models import Employer_job, Employer_jobquestion, Employer_job_Applied, Employer_job_Like, \
    Employer_job_Saved


class SignUpView(View):
    form_class = SignUpForm

    template_name = 'jobseeker/signup.html'

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
                user.is_candidate = True
                user.save()
                new_candidate = Candidate(user=user, is_email_verified=False)  # change is email to False after testing
                new_candidate.save()
                current_site = get_current_site(request)
                subject = 'Activate Your WorkAdaptar Account'
                message = render_to_string('emails/account_activation_email.html', {
                    'user': user,
                    'domain': current_site.domain,
                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                    'token': account_activation_token.make_token(user),
                })
                user.email_user(subject, message)
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

            pr = Candidate.objects.get(user=user)
            pr.is_email_verified = True
            pr.save()
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('home')
        else:
            messages.warning(
                request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('home')


def index(request):
    return render(request, 'index.html')


def login_candidate(request):
    if request.user.is_authenticated and request.user.is_candidate:
        print(request.user)
        return redirect('jobseeker_home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('pass')
            # print(username)
            # print(password)
            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_candidate:
                login(request, user)
                return redirect('jobseeker_home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'jobseeker/login.html', context)


def jobseeker_Home(request):
    c = Candidate.objects.get(user=request.user)
    if Candidate_profile.objects.get(user_id=c):

        job = Employer_job.objects.all()
        a = Employer_job_Applied.objects.filter(candidate_id=c)
        s = Employer_job_Saved.objects.filter(candidate_id=c)
        for j in job:
            if (j in a) or (j in s):
                job.exclude(j)
            else:
                continue

        return render(request, 'home', {'jobs': job})
    else:
        return redirect('create_profile')


# class ProfileRegister(View):
#     form_class = ProfileRegisterForm
#
#     template_name = 'account/signup.html'
#
#     def post(self, request, *args, **kwargs):
#         c = Candidate.objects.get(user=request.user)
#         form = self.form_class(request.POST)
#         if form.is_valid():
#             f = form.save(commit=False)
#             f.user_id = c
#             f.save()
#
#         return redirect('dashboard_home')
def ProfileView(request):
    u = request.user
    c = Candidate.objects.get(user=u)
    profile = Candidate_profile.objects.get(user_id=c)
    edu = Candidate_edu.objects.filter(user_id=c)
    professional = Candidate_profdetail.objects.filter(user_id=c)
    # resume = Candidate_resume.objects.get(user_id=c)
    skills = Candidate_skills.objects.filter(user_id=c)
    return render(request, 'jobseeker/skills.html', {
        "user": u,
        "profile": profile,
        "edu": edu,
        "professional": professional,
        # "resume": resume,
        "skills": skills,
    })


# @login_required(login_url='/login/')
def ProfileEdit(request, pk):
    profile = Candidate.objects.get(user=User_custom.objects.get(id=pk))
    if request.method == 'POST':
        form1 = ProfileRegisterForm(request.POST)
        if form1.is_valid():
            f1 = form1.save(commit=False)
            f1.user_id = profile
        form2 = ProfileRegisterForm_edu(request.POST)
        if form2.is_valid():
            f2 = form2.save(commit=False)
            f2.user_id = profile
        form3 = ProfileRegisterForm_profdetail(request.POST)
        if form3.is_valid():
            f3 = form3.save(commit=False)
            f3.user_id = profile
        form4 = ProfileRegisterForm_resume(request.POST)
        if form4.is_valid():
            f4 = form4.save(commit=False)
            f4.user_id = profile
    form1 = ProfileRegisterForm()
    form2 = ProfileRegisterForm_edu()
    form3 = ProfileRegisterForm_profdetail()
    form4 = ProfileRegisterForm_resume()

    return render(request, 'jobseeker/skills.html',
                  {"form1": form1, 'form2': form2, "form3": form3, 'form4': form4})


class JobApplyView(View):
    template_name = 'dashboard/'

    def get(self, request, pk, *args, **kwargs):
        j = Employer_job.objects.get(pk=pk)
        jq = Employer_jobquestion.objects.filter(job_id=j)
        return render(request, self.template_name, {'jobq': jq})

    def post(self, request, pk, *args, **kwargs):
        pass


def SavedJobs(request):
    c = Candidate.objects.get(user=request.user)
    s = Employer_job_Saved.objects.filter(candidate_id=c)
    return render(request, 'home', {'jobs': s})


def AppliedJobs(request):
    c = Candidate.objects.get(user=request.user)
    a = Employer_job_Applied.objects.filter(candidate_id=c)
    return render(request, 'home', {'jobs': a})
