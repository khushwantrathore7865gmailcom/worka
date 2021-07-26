from datetime import datetime

from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from user_custom.models import User_custom
from django.utils.encoding import force_text
from .models import Candidate, Candidate_profile, Candidate_edu, Candidate_skills, Candidate_profdetail, \
    Candidate_resume
from .forms import SignUpForm, ProfileRegisterForm, ProfileRegisterForm_edu, ProfileRegisterForm_profdetail, \
    ProfileRegisterForm_resume, ProfileRegistration_expdetail, ProfileRegistration_skills
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
    Employer_job_Saved, Employer_candidate_jobanswer, Employer_expired_job, Employer_profile


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
                # subject = 'Activate Your WorkAdaptar Account'
                # message = render_to_string('emails/account_activation_email.html', {
                #     'user': user,
                #     'domain': current_site.domain,
                #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                #     'token': account_activation_token.make_token(user),
                # })
                # user.email_user(subject, message)
                messages.success(
                    request, ('Please check your mail for complete registration.'))
                return redirect('jobseeker:jobseeker/login')
                # return render(request, self.template_name, {'form': form})
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
            return redirect('jobseeker:home')
        else:
            messages.warning(
                request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('jobseeker:home')


def index(request):
    return render(request, 'index.html')


def login_candidate(request):
    if request.user.is_authenticated and request.user.is_candidate:
        print(request.user)
        return redirect('jobseeker:jobseeker_home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('pass')
            # print(username)
            # print(password)
            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_candidate:
                login(request, user)
                return redirect('jobseeker:jobseeker_home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'jobseeker/login.html', context)


def jobseeker_Home(request):
    if request.method == 'POST':
        print(request.POST)
        pk = request.POST.get('pk')
        print(pk)
        c = Candidate.objects.get(user=request.user)
        job = Employer_job.objects.get(pk=pk)
        questions = Employer_jobquestion.objects.filter(job_id=job)
        for q in questions:
            print(request.POST.get(q.question))

            get_text = request.POST.get(q.question)
            print(get_text)
            Employer_candidate_jobanswer.objects.create(candidate_id=c, question_id=q, answer=get_text).save()
        Employer_job_Applied.objects.create(candidate_id=c, job_id=job).save()
    jobs = []
    job_ques = []
    relevant_jobs = []
    common = []
    companyprofile = []
    job_skills = []
    u = request.user
    c = Candidate.objects.get(user=u)
    try:
        cp = Candidate_profile.objects.get(user_id=c)
    except Candidate_profile.DoesNotExist:
        cp = None

    # if u.first_login:

    skills = Candidate_skills.objects.filter(user_id=c)

    my_sk = []
    j = 0
    for i in skills:
        my_sk.insert(j, i.skill.lower())
        j = j + 1
    job = Employer_job.objects.all()
    for j in job:
        start_date = j.created_on
        # print(start_date)
        today = datetime.now()
        # print(type(today))
        stat_date = str(start_date)
        start_date = stat_date[:19]
        tday = str(today)
        today = tday[:19]
        s_date = datetime.strptime(start_date, "%Y-%m-%d %H:%M:%S")
        e_date = datetime.strptime(today, "%Y-%m-%d %H:%M:%S")
        # print(s_date)
        # print(e_date)
        diff = abs((e_date - s_date).days)
        print(diff)
        if diff > 30:
            # expired_job.append(j)
            Employer_expired_job.objects.create(job_id=j).save()

        else:
            jobs.append(j)

    for job in jobs:
        skills = []
        sk = str(job.skill).split(",")
        for i in sk:
            skills.append(i.strip().lower())
        common_skills = list(set(my_sk) & set(skills))
        if len(common_skills) != 0:
            e = job.employer_id
            companyprofile.append(Employer_profile.objects.get(employer=e))
            try:
                userS = Employer_job_Saved.objects.get(job_id=job.pk, candidate_id=c)
                # print(userS.job_id)
            except Employer_job_Saved.DoesNotExist:
                userS = None
            try:
                userA = Employer_job_Applied.objects.get(job_id=job.pk, candidate_id=c)
                # print(userA.job_id)
            except Employer_job_Applied.DoesNotExist:
                userA = None

            if userA:
                # print(userA)
                continue
            if userS:
                # print(userS)
                continue
            relevant_jobs.append(job)
            common.append(len(common_skills))
            job_skills.append(len(skills))
            job_ques.append(Employer_jobquestion.objects.filter(job_id=job))

            print(job_ques)

    objects = zip(relevant_jobs, common, job_skills, job_ques, companyprofile)

    return render(request, 'jobseeker/home.html', {'jobs': objects, 'c': c, 'cp': cp})
    # else:
    #     u.first_login=True
    #       u.save()
    #     return redirect('jobseeker:ProfileEdit')


def save_later(request, pk):
    c = Candidate.objects.get(user=request.user)
    job = Employer_job.objects.get(pk=pk)
    # print(c)
    # print(job)
    Employer_job_Saved.objects.create(job_id=job, candidate_id=c).save()
    return redirect('jobseeker:jobseeker_home')


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
    resume = Candidate_resume.objects.get(user_id=c)
    skills = Candidate_skills.objects.filter(user_id=c)
    return render(request, 'jobseeker/skills.html', {
        "user": u,
        "profile": profile,
        "edu": edu,
        "professional": professional,
        "resume": resume,
        "skills": skills,
    })


# @login_required(login_url='/login/')
def ProfileEdit(request):
    profile = Candidate.objects.get(user=request.user)
    if request.method == 'POST':
        form1 = ProfileRegisterForm(request.POST)
        form2 = ProfileRegisterForm_edu(request.POST)
        form3 = ProfileRegisterForm_profdetail(request.POST)
        form4 = ProfileRegisterForm_resume(request.POST)
        form5 = ProfileRegistration_skills(request.POST)
        form6 = ProfileRegistration_expdetail(request.POST)
        if form1.is_valid() and form2.is_valid() and form3.is_valid() and form4.is_valid() and form5.is_valid() and form6.is_valid():
            f1 = form1.save(commit=False)
            f1.user_id = profile
            f1.save()

            f2 = form2.save(commit=False)
            if f2.cleaned_data.get('institute_name'):
                f2.user_id = profile
                f2.save()

            f3 = form3.save(commit=False)
            if f2.cleaned_data.get('designation'):
                f3.user_id = profile
                f3.save()

            f4 = form4.save(commit=False)
            f4.user_id = profile
            f4.save()

            f5 = form5.save(commit=False)
            f5.user_id = profile
            f5.save()

            f6 = form6.save(commit=False)
            f6.user_id = profile
            f6.save()
            return redirect('jobseeker:jobseeker_home')

    form1 = ProfileRegisterForm()
    form2 = ProfileRegisterForm_edu(queryset=Candidate_edu.objects.none())
    form3 = ProfileRegisterForm_profdetail(queryset=Candidate_profdetail.objects.none())
    form4 = ProfileRegisterForm_resume()
    form5 = ProfileRegistration_skills()
    form6 = ProfileRegistration_expdetail()

    return render(request, 'jobseeker/Profile.html',
                  {"form1": form1, 'form2': form2, "form3": form3, 'form4': form4, "form5": form5, 'form6': form6})


def SavedJobs(request):
    if request.method == 'POST':
        print(request.POST)
        pk = request.POST.get('pk')
        print(pk)
        c = Candidate.objects.get(user=request.user)
        job = Employer_job.objects.get(pk=pk)
        questions = Employer_jobquestion.objects.filter(job_id=job)
        for q in questions:
            print(request.POST.get(q.question))

            get_text = request.POST.get(q.question)
            print(get_text)
            Employer_candidate_jobanswer.objects.create(candidate_id=c, question_id=q, answer=get_text).save()
        Employer_job_Applied.objects.create(candidate_id=c, job_id=job).save()

    job_ques = []
    companyprofile = []
    relevant_jobs = []
    common = []
    job_skills = []
    my_sk = []
    c = Candidate.objects.get(user=request.user)
    try:
        cp=Candidate_profile.objects.get(user_id=c)
    except Candidate_profile.DoesNotExist:
        cp=None
    if cp:
        skills = Candidate_skills.objects.filter(user_id=c)



        j = 0
        for i in skills:
            my_sk.insert(j, i.skill.lower())
            j = j + 1
        jobs = Employer_job.objects.all()

        for job in jobs:
            skills = []
            sk = str(job.skill).split(",")
            for i in sk:
                skills.append(i.strip().lower())
            common_skills = list(set(my_sk) & set(skills))
            if len(common_skills) != 0:
                try:
                    userS = Employer_job_Saved.objects.get(job_id=job.pk, candidate_id=c)
                    # print(userS.job_id)
                except Employer_job_Saved.DoesNotExist:
                    userS = None
                # try:
                #     userA = Employer_job_Applied.objects.get(job_id=job.pk, candidate_id=c)
                #     # print(userA.job_id)
                # except Employer_job_Applied.DoesNotExist:
                #     userA = None

                # if userA:
                #     # print(userA)
                #     continue
                if userS:
                    e = job.employer_id
                    companyprofile.append(Employer_profile.objects.get(employer=e))
                    # print(userS)
                    # continue
                    relevant_jobs.append(job)
                    common.append(len(common_skills))
                    job_skills.append(len(skills))
                    job_ques.append(Employer_jobquestion.objects.filter(job_id=job))

                print(relevant_jobs)

        objects = zip(relevant_jobs, common, job_skills, job_ques, companyprofile)

        return render(request, 'jobseeker/savedjobs.html', {'jobs': objects})
    else:
        return render(request, 'jobseeker/savedjobs.html')


def AppliedJobs(request):
    companyprofile = []
    c = Candidate.objects.get(user=request.user)
    applied = Employer_job_Applied.objects.filter(candidate_id=c)
    for a in applied:
        e = a.job_id.employer_id
        companyprofile.append(Employer_profile.objects.get(employer=e))

    objects = zip(applied, companyprofile)
    return render(request, 'jobseeker/applied.html', {'jobs': objects})


def remove_applied(request, pk):
    Employer_job_Applied.objects.get(pk=pk).delete()

    return redirect('jobseeker:AppliedJobs')


def remove_saved(request, pk):
    c = Candidate.objects.get(user=request.user)
    job = Employer_job.objects.get(pk=pk)
    savej = Employer_job_Saved.objects.filter(job_id=job)
    for s in savej:
        if s.candidate_id == c:
            s.delete()

    return redirect('jobseeker:SavedJobs')
