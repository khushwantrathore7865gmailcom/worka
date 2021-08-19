from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from user_custom.models import User_custom
from django.utils.encoding import force_text
from .models import Employer, Employer_profile, Employer_candidate_jobanswer, Employer_job, Employer_job_Applied, \
    Employer_jobquestion, Employer_expired_job
from .forms import SignUpForm, ProfileRegisterForm, JobPostForm, JobsQuestionForm, QuestionFormset
from django.views.generic import View
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth import login, authenticate
from django.shortcuts import render, redirect, get_object_or_404
from .tokens import account_activation_token
from jobseeker.models import Candidate_profile, Candidate_edu, Candidate_profdetail, Candidate_resume, Candidate_skills, \
    Candidate_expdetail
from datetime import datetime
from django.forms import modelformset_factory
from django.db import transaction, IntegrityError


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
                user.user_name = user.email
                user.is_active = True  # change this to False after testing
                user.is_employeer = True
                user.save()
                new_employe = Employer(user=user, is_email_verified=False)
                new_employe.save()
                # current_site = get_current_site(request)
                # subject = 'Activate Your WorkAdaptar Account'
                # message = render_to_string('emails/account_activation_email.html', {
                #     'user': user,
                #     'domain': current_site.domain,
                #     'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                #     'token': account_activation_token.make_token(new_employe),
                # })
                # user.email_user(subject, message)
                messages.success(
                    request, ('Please check your mail for complete registration.'))
                return redirect('recruiter:employer/login')
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

            pr = Employer.objects.get(user=user)
            pr.is_email_verified = True
            pr.save()
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('recruiter:dashboard_home')
        else:
            messages.warning(
                request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('recruiter:dashboard_home')


def login_employer(request):
    if request.user.is_authenticated and request.user.is_employeer:
        print(request.user)
        return redirect('recruiter:employer_home')
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
                return redirect('recruiter:employer_home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'employer/login.html', context)


def Home(request):
    jobs = []
    expired_job = []

    try:
        e = Employer.objects.get(user=request.user)
    except Employer.DoesNotExist:
        e = None
    # uncomment this after making the profile update correct
    # if Employer_profile.objects.get(employer=e):
    if e:
        try:
            ep = Employer_profile.objects.get(employer=e)
        except Employer_profile.DoesNotExist:
            ep = None
        job = Employer_job.objects.filter(employer_id=e)
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
            try:
                e_j = Employer_expired_job.objects.get(job_id=j)
            except Employer_expired_job.DoesNotExist:
                e_j = None
            if diff > 30:
                if e_j:
                    expired_job.append(j)
                else:
                    Employer_expired_job.objects.create(job_id=j).save()
                    expired_job.append(j)
            elif e_j:
                expired_job.append(j)
            else:
                jobs.append(j)
        context = {'jobs': jobs, 'expired': expired_job, 'ep': ep}
        return render(request, 'employer/job-post.html', context)
    else:
        return redirect('recruiter:employer/login')


def edit_job(request, pk):
    user = request.user
    job = get_object_or_404(Employer_job, pk=pk)
    if request.method == "POST":
        form = JobPostForm(request.POST, instance=job)
        if form.is_valid():
            data = form.save(commit=False)
            data.save()
            return redirect('recruiter:employer_home')
    else:
        form = JobPostForm(instance=job)
    context = {
        'form': form,
        'rec_navbar': 1,
        'job': job,
    }
    return render(request, 'employer/edit_job.html', context)


def job_detail(request, pk):
    e = Employer.objects.get(user=request.user)
    job = Employer_job.objects.get(pk=pk)
    company = Employer_profile.objects.get(employer=e)
    # candidate_Applied = Employer_job_Applied.objects.filter(job_id=job)
    # objects = zip(job,candidate_Applied)
    return render(request, 'employer/job_details.html', {'job': job, 'c': company})


def view_applied_candidate(request, pk):
    candidate_user = []
    candidate_profile = []
    education_profile = []
    professional_profile = []
    skill = []
    resume = []
    expect = []
    candidate_answer = []
    # Question=[]
    e = Employer.objects.get(user=request.user)
    job = Employer_job.objects.get(pk=pk)
    question = Employer_jobquestion.objects.filter(job_id=job)
    candidate_Applied = Employer_job_Applied.objects.filter(job_id=job)
    for can in candidate_Applied:
        c = can.candidate_id
        candidate_profile.append(Candidate_profile.objects.get(user_id=c))
        candidate_user.append(c.user)
        education_profile.append(Candidate_edu.objects.filter(user_id=c).first())
        professional_profile.append(Candidate_profdetail.objects.filter(user_id=c))
        expect.append(Candidate_expdetail.objects.get(user_id=c))
        skill.append(Candidate_skills.objects.filter(user_id=c))

        resume.append(Candidate_resume.objects.get(user_id=c))
        for q in question:
            candidate_answer.append(Employer_candidate_jobanswer.objects.get(question_id=q, candidate_id=c))

    quest = zip(question, candidate_answer)
    # print(candidate_answer)
    objects = zip(candidate_profile, education_profile, professional_profile, skill, resume,
                  candidate_user, candidate_Applied, expect)

    return render(request, 'employer/job_candidate.html',
                  {'candidate': objects, 'job': job, 'question': question, 'answer': candidate_answer})
    # return render(request, 'employer/job_candidate.html',
    #               {'candidate': objects, 'job': job, 'quest': quest})


def shortlistview_applied_candidate(request, pk):
    candidate_user = []
    candidate_profile = []
    education_profile = []
    professional_profile = []
    skill = []
    resume = []
    candidate_answer = []
    expect = []
    e = Employer.objects.get(user=request.user)
    job = Employer_job.objects.get(pk=pk)
    question = Employer_jobquestion.objects.filter(job_id=job)
    candidate_Applied = Employer_job_Applied.objects.filter(job_id=job)
    for can in candidate_Applied:
        c = can.candidate_id
        candidate_profile.append(Candidate_profile.objects.get(user_id=c))
        candidate_user.append(c.user)
        education_profile.append(Candidate_edu.objects.filter(user_id=c))
        professional_profile.append(Candidate_profdetail.objects.filter(user_id=c))

        skill.append(Candidate_skills.objects.filter(user_id=c))
        expect.append(Candidate_expdetail.objects.get(user_id=c))
        resume.append(Candidate_resume.objects.get(user_id=c))
        for q in question:
            candidate_answer.append(Employer_candidate_jobanswer.objects.get(question_id=q, candidate_id=c))

    objects = zip(candidate_profile, education_profile, professional_profile, skill, resume,
                  candidate_user, candidate_Applied, expect)
    # question = zip(question, candidate_answer)
    return render(request, 'employer/shortlisted_view.html',
                  {'candidate': objects, 'job': job, 'question': question, 'answer': candidate_answer})


def disqualifyview_applied_candidate(request, pk):
    candidate_user = []
    candidate_profile = []
    education_profile = []
    professional_profile = []
    skill = []
    resume = []
    expect = []
    candidate_answer = []
    e = Employer.objects.get(user=request.user)
    job = Employer_job.objects.get(pk=pk)
    question = Employer_jobquestion.objects.filter(job_id=job)
    candidate_Applied = Employer_job_Applied.objects.filter(job_id=job)
    for can in candidate_Applied:
        c = can.candidate_id
        candidate_profile.append(Candidate_profile.objects.get(user_id=c))
        candidate_user.append(c.user)
        education_profile.append(Candidate_edu.objects.filter(user_id=c))
        professional_profile.append(Candidate_profdetail.objects.filter(user_id=c))
        expect.append(Candidate_expdetail.objects.get(user_id=c))
        skill.append(Candidate_skills.objects.filter(user_id=c))

        resume.append(Candidate_resume.objects.get(user_id=c))
        for q in question:
            candidate_answer.append(Employer_candidate_jobanswer.objects.get(question_id=q, candidate_id=c))

    objects = zip(candidate_profile, education_profile, professional_profile, skill, resume,
                  candidate_user, candidate_Applied, expect)
    # question = zip(question, candidate_answer)
    return render(request, 'employer/disqualified.html',
                  {'candidate': objects, 'job': job, 'question': question, 'answer': candidate_answer})


def shortlist(request, pk):
    e = Employer_job_Applied.objects.get(pk=pk)
    e.is_shortlisted = True
    e.is_disqualified = False
    e.save()
    print(e.job_id.pk)
    return redirect('recruiter:view_applied_candidate', e.job_id.pk)


def disqualify(request, pk):
    e = Employer_job_Applied.objects.get(pk=pk)
    e.is_shortlisted = False
    e.is_disqualified = True
    e.save()
    print(e.job_id.pk)
    return redirect('recruiter:view_applied_candidate', e.job_id.pk)


def delete_job(request, pk):
    Employer_job.objects.get(pk=pk).delete()

    return redirect('recruiter:employer_home')


def publish_job(request, pk):
    e = Employer_job.objects.get(pk=pk)
    e.is_save_later = False
    e.save()
    return redirect('recruiter:job_detail', pk)


# @login_required(login_url='/login/')
def ProfileView(request):
    u = request.user
    e = Employer.objects.get(user=u)
    profile = Employer_profile.objects.get(employer=e)

    return render(request, 'employer/skills.html', {
        "user": u,
        "profile": profile,

    })


def job_post(request):
    e = Employer.objects.get(user=request.user)
    if request.method == 'GET':
        form1 = JobPostForm(request.GET or None)
        formset = QuestionFormset(request.GET or None)
    elif request.method == 'POST':
        form1 = JobPostForm(request.POST)
        formset = QuestionFormset(request.POST)
        if form1.is_valid():
            f1 = form1.save(commit=False)
            f1.employer_id = e
            f1.save()
            # print(f1)
        if formset.is_valid():
            # print("formset:")
            # print(formset)
            for form in formset:
                # print("form:")
                # print(form)
                quest = form.cleaned_data.get('question')
                # print("question:")
                # print(quest)
                if quest:
                    Employer_jobquestion(job_id=f1, question=quest).save()

            return redirect('recruiter:employer_home')
    #
    #         form2 = JobsQuestionForm(request.POST)
    #         if form2.is_valid():
    #             f2 = form2.save(commit=False)
    #             f2.employer_id = e
    #             f2.job_id = f1
    #             f2.save()
    #             f1.save()
    # form1 = JobPostForm(request.POST)
    # form2 = JobsQuestionForm(request.POST)
    return render(request, 'employer/addjob.html', {"form1": form1, "form2": formset})


def job_Response(request, pk):
    job = Employer_job.objects.get(pk=pk)
    response = Employer_job_Applied.objects.filter(job_id=job)
    return render(request, 'dashboard/jobresponse.html', {'response': response})
