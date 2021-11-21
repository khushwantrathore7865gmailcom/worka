import re
from datetime import datetime
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.http import HttpResponse, HttpResponseRedirect
from django.utils.datastructures import MultiValueDictKeyError
from django.utils.http import urlsafe_base64_decode
from user_custom.models import User_custom
from django.utils.encoding import force_text
from .models import Candidate, Candidate_profile, Candidate_edu, Candidate_skills, Candidate_profdetail, \
    Candidate_resume, Resume_order, Candidate_expdetail,Resume_headline
from .forms import SignUpForm, ProfileRegisterForm, ProfileRegisterForm_edu, ProfileRegisterForm_profdetail, \
    ProfileRegisterForm_resume, ProfileRegistration_expdetail, ProfileRegistration_skills, Resumeforming_Entery, \
    Resumeforming_Executive, Resumeforming_Mid, Resumeforming_senior,Resume_headlineForm
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

import razorpay
from django.contrib.auth.decorators import login_required

client = razorpay.Client(auth=("rzp_test_N6naZCMdnNcNcU", "pdkCmhFp28iS6acXCLJuyPFb"))


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
            # print(form.password1)
            if User_custom.objects.filter(email=emaill).exists():

                return HttpResponse('User with same email already exists, Please try again with different Username!!')
            else:
                user = form.save(commit=False)
                user.username = user.email
                user.user_name = user.email
                user.is_active = True  # change this to False after testing
                user.is_candidate = True
                user.save()
                new_candidate = Candidate(user=user, is_email_verified=False)  # change is email to False after testing
                new_candidate.save()

                username = form.cleaned_data['email']
                password = form.cleaned_data['password1']

                # print(username)
                # print(password)
                user = authenticate(request, username=username, password=password)

                if user is not None and user.is_candidate:
                    login(request, user)
                    return redirect('jobseeker:jobseeker_home')
                # return render(request, self.template_name, {'form': form})
        else:
            return render(request, self.template_name, {'form': form})


def sendVerificationMail(request):
    user = request.user
    current_site = get_current_site(request)
    subject = 'Activate Your WorkAdaptar Account'
    message = render_to_string('emails/account_activation_jobseeker.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': account_activation_token.make_token(user),
    })
    user.email_user(subject, message)
    messages.success(
        request, ('Please check your mail for complete registration.'))
    return redirect('jobseeker:jobseeker_home')


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
            return redirect('jobseeker:jobseeker_home')
        else:
            messages.warning(
                request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('jobseeker:jobseeker_home')


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
            Pattern = re.compile("(0|91)?[0-9]{10}")
            if Pattern.match(username):
                c = Candidate_profile.objects.get(phone=username)
                username = c.employer.user.username
            # print(username)
            # print(password)
            user = authenticate(request, username=username, password=password)

            if user is not None and user.is_candidate:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('jobseeker:jobseeker_home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'index.html', context)
        # return render(request, 'jobseeker/login.html', context)


@login_required(login_url='/')
def jobseeker_Home(request):
    if request.method == 'GET':
        val = request.GET.get('search_box', None)
        print("val")
        print(val)
        if val:
            job = Employer_job.objects.filter(
                Q(job_title__icontains=val) |
                Q(skill__icontains=val) |
                Q(job_description__icontains=val) |
                Q(job_salary__icontains=val) |
                Q(job_location__icontains=val)
            ).distinct()
            print(job)
            jobs = []
            job_ques = []
            relevant_jobs = []
            common = []
            companyprofile = []
            job_skills = []
            u = request.user
            if u is not None and u.is_candidate:
                c = Candidate.objects.get(user=u)
                try:
                    cp = Candidate_profile.objects.get(user_id=c)
                except Candidate_profile.DoesNotExist:
                    cp = None
                try:
                    cep = Candidate_expdetail.objects.get(user_id=c)
                except Candidate_expdetail.DoesNotExist:
                    cep = None
                try:
                    cr = Candidate_resume.objects.get(user_id=c)
                except Candidate_resume.DoesNotExist:
                    cr = None
                if u.first_login:

                    skills = Candidate_skills.objects.filter(user_id=c)
                    print("skills")
                    print(skills)
                    if len(skills) != 0:

                        my_sk = []
                        j = 0
                        for i in skills:
                            my_sk.insert(j, i.skill.lower())
                            j = j + 1

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

                        pj = Paginator(relevant_jobs, 5)
                        pjt = Paginator(relevant_jobs, 5)
                        pc = Paginator(common, 5)
                        pjs = Paginator(job_skills, 5)
                        pjq = Paginator(job_ques, 5)
                        pcp = Paginator(companyprofile, 5)
                        page_num = request.GET.get('page', 1)
                        try:
                            pj_objects = pj.page(page_num)
                            pjt_objects = pjt.page(page_num)
                            pc_objects = pc.page(page_num)
                            pjs_objects = pjs.page(page_num)
                            pjq_objects = pjq.page(page_num)
                            pcp_objects = pcp.page(page_num)
                        except EmptyPage:
                            pj_objects = pj.page(1)
                            pjt_objects = pjt.page(1)
                            pc_objects = pc.page(1)
                            pjs_objects = pjs.page(1)
                            pjq_objects = pjq.page(1)
                            pcp_objects = pcp.page(1)
                        objects = zip(pj_objects, pc_objects, pjs_objects, pjq_objects, pcp_objects)

                        return render(request, 'jobseeker/home.html',
                                      {'jobs': objects, 'c': c, 'cp': cp, 'cep': cep, 'cr': cr, 'pjs': pjt_objects})
                    else:

                        print("len job")
                        print(len(job))
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
                            # print(diff)
                            if diff > 30:
                                # expired_job.append(j)
                                Employer_expired_job.objects.create(job_id=j).save()

                            else:
                                jobs.append(j)
                            print("len")
                            print(len(jobs))
                        for jo in jobs:
                            skills = []
                            sk = str(jo.skill).split(",")
                            for i in sk:
                                skills.append(i.strip().lower())
                            common_skill = []
                            e = jo.employer_id
                            companyprofile.append(Employer_profile.objects.get(employer=e))
                            try:
                                userS = Employer_job_Saved.objects.get(job_id=jo.pk, candidate_id=c)
                                # print(userS.job_id)
                            except Employer_job_Saved.DoesNotExist:
                                userS = None
                            try:
                                userA = Employer_job_Applied.objects.get(job_id=jo.pk, candidate_id=c)
                                # print(userA.job_id)
                            except Employer_job_Applied.DoesNotExist:
                                userA = None

                            if userA:
                                # print(userA)
                                continue
                            if userS:
                                # print(userS)
                                continue
                            relevant_jobs.append(jo)
                            print("job:")
                            print(jo)

                            common.append(len(common_skill))
                            job_skills.append(len(skills))
                            job_ques.append(Employer_jobquestion.objects.filter(job_id=jo))
                        print("job_quest:")
                        print(job_ques)
                        print("relevant_jobs")
                        print(len(relevant_jobs))
                        pj = Paginator(relevant_jobs, 5)
                        pjt = Paginator(relevant_jobs, 5)
                        pc = Paginator(common, 5)
                        pjs = Paginator(job_skills, 5)
                        pjq = Paginator(job_ques, 5)
                        pcp = Paginator(companyprofile, 5)
                        page_num = request.GET.get('page', 1)
                        try:
                            pj_objects = pj.page(page_num)
                            pjt_objects = pjt.page(page_num)
                            pc_objects = pc.page(page_num)
                            pjs_objects = pjs.page(page_num)
                            pjq_objects = pjq.page(page_num)
                            pcp_objects = pcp.page(page_num)
                        except EmptyPage:
                            pj_objects = pj.page(1)
                            pjt_objects = pjt.page(1)
                            pc_objects = pc.page(1)
                            pjs_objects = pjs.page(1)
                            pjq_objects = pjq.page(1)
                            pcp_objects = pcp.page(1)
                        objects = zip(pj_objects, pc_objects, pjs_objects, pjq_objects, pcp_objects)

                        return render(request, 'jobseeker/home.html',
                                      {'jobs': objects, 'c': c, 'cp': cp, 'cep': cep, 'cr': cr, 'pjs': pjt_objects})


        else:
            jobs = []
            job_ques = []
            relevant_jobs = []
            common = []
            companyprofile = []
            job_skills = []
            u = request.user
            if u is not None and u.is_candidate:
                c = Candidate.objects.get(user=u)
                try:
                    cp = Candidate_profile.objects.get(user_id=c)
                except Candidate_profile.DoesNotExist:
                    cp = None
                try:
                    cep = Candidate_expdetail.objects.get(user_id=c)
                except Candidate_expdetail.DoesNotExist:
                    cep = None
                try:
                    cr = Candidate_resume.objects.get(user_id=c)
                except Candidate_resume.DoesNotExist:
                    cr = None
                if u.first_login:

                    skills = Candidate_skills.objects.filter(user_id=c)
                    print(skills)
                    if len(skills) != 0:

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
                        pj = Paginator(relevant_jobs, 5)
                        pjt = Paginator(relevant_jobs, 5)
                        pc = Paginator(common, 5)
                        pjs = Paginator(job_skills, 5)
                        pjq = Paginator(job_ques, 5)
                        pcp = Paginator(companyprofile, 5)
                        page_num = request.GET.get('page', 1)
                        try:
                            pj_objects = pj.page(page_num)
                            pjt_objects = pjt.page(page_num)
                            pc_objects = pc.page(page_num)
                            pjs_objects = pjs.page(page_num)
                            pjq_objects = pjq.page(page_num)
                            pcp_objects = pcp.page(page_num)
                        except EmptyPage:
                            pj_objects = pj.page(1)
                            pjt_objects = pjt.page(1)
                            pc_objects = pc.page(1)
                            pjs_objects = pjs.page(1)
                            pjq_objects = pjq.page(1)
                            pcp_objects = pcp.page(1)
                        objects = zip(pj_objects, pc_objects, pjs_objects, pjq_objects, pcp_objects)

                        return render(request, 'jobseeker/home.html',
                                      {'jobs': objects, 'c': c, 'cp': cp, 'cep': cep, 'cr': cr, 'pjs': pjt_objects})
                    else:
                        job = Employer_job.objects.all()
                        print("len job")
                        print(len(job))
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
                            # print(diff)
                            if diff > 30:
                                # expired_job.append(j)
                                Employer_expired_job.objects.create(job_id=j).save()

                            else:
                                jobs.append(j)
                            print("len")
                            print(len(jobs))
                        for jo in jobs:
                            skills = []
                            sk = str(jo.skill).split(",")
                            for i in sk:
                                skills.append(i.strip().lower())
                            common_skill = []
                            e = jo.employer_id
                            companyprofile.append(Employer_profile.objects.get(employer=e))
                            try:
                                userS = Employer_job_Saved.objects.get(job_id=jo.pk, candidate_id=c)
                                # print(userS.job_id)
                            except Employer_job_Saved.DoesNotExist:
                                userS = None
                            try:
                                userA = Employer_job_Applied.objects.get(job_id=jo.pk, candidate_id=c)
                                # print(userA.job_id)
                            except Employer_job_Applied.DoesNotExist:
                                userA = None

                            if userA:
                                # print(userA)
                                continue
                            if userS:
                                # print(userS)
                                continue
                            relevant_jobs.append(jo)
                            print("job:")
                            print(jo)

                            common.append(len(common_skill))
                            job_skills.append(len(skills))
                            job_ques.append(Employer_jobquestion.objects.filter(job_id=jo))
                        print("job_quest:")
                        print(job_ques)
                        print("relevant_jobs")
                        print(len(relevant_jobs))
                        pj = Paginator(relevant_jobs, 5)
                        pjt = Paginator(relevant_jobs, 5)
                        pc = Paginator(common, 5)
                        pjs = Paginator(job_skills, 5)
                        pjq = Paginator(job_ques, 5)
                        pcp = Paginator(companyprofile, 5)
                        page_num = request.GET.get('page', 1)
                        try:
                            pj_objects = pj.page(page_num)
                            pjt_objects = pjt.page(page_num)
                            pc_objects = pc.page(page_num)
                            pjs_objects = pjs.page(page_num)
                            pjq_objects = pjq.page(page_num)
                            pcp_objects = pcp.page(page_num)
                        except EmptyPage:
                            pj_objects = pj.page(1)
                            pjt_objects = pjt.page(1)
                            pc_objects = pc.page(1)
                            pjs_objects = pjs.page(1)
                            pjq_objects = pjq.page(1)
                            pcp_objects = pcp.page(1)
                        objects = zip(pj_objects, pc_objects, pjs_objects, pjq_objects, pcp_objects)

                        return render(request, 'jobseeker/home.html',
                                      {'jobs': objects, 'c': c, 'cp': cp, 'cep': cep, 'cr': cr, 'pjs': pjt_objects})

                else:
                    u.first_login = True
                    u.save()
                    return redirect('jobseeker:create_profile')
            else:
                return redirect('/')

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


@login_required(login_url='/')
def save_later(request, pk):
    c = Candidate.objects.get(user=request.user)
    if c is not None:
        job = Employer_job.objects.get(pk=pk)
        # print(c)
        # print(job)
        Employer_job_Saved.objects.create(job_id=job, candidate_id=c).save()
        return redirect('jobseeker:jobseeker_home')
    else:
        return redirect('/')


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
@login_required(login_url='/')
def ProfileView(request):
    if request.method == 'GET':
        val = request.GET.get('search_box', None)
        print("val")
        print(val)
        if val:
            job = Employer_job.objects.filter(
                Q(job_title__icontains=val) |
                Q(skill__icontains=val) |
                Q(job_description__icontains=val) |
                Q(job_salary__icontains=val) |
                Q(job_location__icontains=val)
            ).distinct()
            print(job)
            jobs = []
            job_ques = []
            relevant_jobs = []
            common = []
            companyprofile = []
            job_skills = []
            u = request.user
            if u is not None and u.is_candidate:
                c = Candidate.objects.get(user=u)
                try:
                    cp = Candidate_profile.objects.get(user_id=c)
                except Candidate_profile.DoesNotExist:
                    cp = None
                try:
                    cep = Candidate_expdetail.objects.get(user_id=c)
                except Candidate_expdetail.DoesNotExist:
                    cep = None
                try:
                    cr = Candidate_resume.objects.get(user_id=c)
                except Candidate_resume.DoesNotExist:
                    cr = None
                if u.first_login:

                    skills = Candidate_skills.objects.filter(user_id=c)
                    print("skills")
                    print(skills)
                    if len(skills) != 0:

                        my_sk = []
                        j = 0
                        for i in skills:
                            my_sk.insert(j, i.skill.lower())
                            j = j + 1

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

                        objects = zip(relevant_jobs, common, job_skills, job_ques, companyprofile)

                        return render(request, 'jobseeker/home.html',
                                      {'jobs': objects, 'c': c, 'cp': cp, 'cep': cep, 'cr': cr})
                    else:

                        print("len job")
                        print(len(job))
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
                            # print(diff)
                            if diff > 30:
                                # expired_job.append(j)
                                Employer_expired_job.objects.create(job_id=j).save()

                            else:
                                jobs.append(j)
                            print("len")
                            print(len(jobs))
                        for jo in jobs:
                            skills = []
                            sk = str(jo.skill).split(",")
                            for i in sk:
                                skills.append(i.strip().lower())
                            common_skill = []
                            e = jo.employer_id
                            companyprofile.append(Employer_profile.objects.get(employer=e))
                            try:
                                userS = Employer_job_Saved.objects.get(job_id=jo.pk, candidate_id=c)
                                # print(userS.job_id)
                            except Employer_job_Saved.DoesNotExist:
                                userS = None
                            try:
                                userA = Employer_job_Applied.objects.get(job_id=jo.pk, candidate_id=c)
                                # print(userA.job_id)
                            except Employer_job_Applied.DoesNotExist:
                                userA = None

                            if userA:
                                # print(userA)
                                continue
                            if userS:
                                # print(userS)
                                continue
                            relevant_jobs.append(jo)
                            print("job:")
                            print(jo)

                            common.append(len(common_skill))
                            job_skills.append(len(skills))
                            job_ques.append(Employer_jobquestion.objects.filter(job_id=jo))
                        print("job_quest:")
                        print(job_ques)
                        print("relevant_jobs")
                        print(len(relevant_jobs))
                        objects = zip(relevant_jobs, common, job_skills, job_ques, companyprofile)
                        return render(request, 'jobseeker/home.html',
                                      {'jobs': objects, 'c': c, 'cp': cp, 'cep': cep, 'cr': cr})
        else:
            u = request.user
            c = Candidate.objects.get(user=u)
            try:
                profile = Candidate_profile.objects.get(user_id=c)
            except Candidate_profile.DoesNotExist:
                profile = None
            try:
                edu = Candidate_edu.objects.filter(user_id=c)
            except Candidate_edu.DoesNotExist:
                edu = None
            try:
                professional = Candidate_profdetail.objects.filter(user_id=c)
            except Candidate_profdetail.DoesNotExist:
                professional = None
            try:
                resume = Candidate_resume.objects.get(user_id=c)
            except Candidate_resume.DoesNotExist:
                resume = None

            try:
                skills = Candidate_skills.objects.filter(user_id=c)
            except Candidate_skills.DoesNotExist:
                skills = None
            return render(request, 'jobseeker/skills.html', {
                "user": u,
                "profile": profile,
                "edu": edu,
                "professional": professional,
                "resume": resume,
                "skills": skills,
            })


@login_required(login_url='/')
def ProfileEdit(request):
    try:
        profile = Candidate.objects.get(user=request.user)
    except Candidate.DoesNotExist:
        profile = None
    print(profile)
    if profile is not None:
        if request.method == 'POST':
            form1 = ProfileRegisterForm(data=request.POST or None, files=request.FILES or None)
            form2 = ProfileRegisterForm_edu(request.POST or None)
            form3 = ProfileRegisterForm_profdetail(request.POST or None)
            form4 = ProfileRegisterForm_resume(request.POST or None)
            form5 = ProfileRegistration_skills(request.POST or None)
            form6 = ProfileRegistration_expdetail(request.POST or None)
            form7 = Resume_headlineForm(request.POST)
            form8 = ProfileRegistration_skills(request.POST)
            # print(form1)
            if form1.is_valid():
                print(form1.cleaned_data.get('profile_pic'))
                if form1.cleaned_data.get('birth_date'):
                    f1 = form1.save(commit=False)
                    try:
                        c = Candidate_profile.objects.get(user_id=profile)
                    except Candidate_profile.DoesNotExist:
                        c = None
                    if c:
                        c.delete()

                    f1.user_id = profile

                    f1.save()

            if form2.is_valid():
                f2 = form2.save(commit=False)
                if form2.cleaned_data.get('institute_name'):
                    f2.user_id = profile
                    f2.save()
            if form3.is_valid():
                f3 = form3.save(commit=False)
                if form3.cleaned_data.get('designation'):
                    f3.user_id = profile
                    f3.save()
            if form4.is_valid():
                f4 = form4.save(commit=False)
                f4.user_id = profile
                try:
                    f=request.FILES['resume_link']
                except MultiValueDictKeyError:
                    f = False
                if f is not False:
                    f4.resume_link=f
                    f4.save()

                # f5 = form5.save(commit=False)
                # f5.user_id = profile
                # f5.save()

                # for form in form5:
                #     # extract name from each form and save
                #     skill = form.cleaned_data.get('skill')
                #     rating = form.cleaned_data.get('rating')
                #     # save book instance
                #     if skill:
                #         Candidate_skills(user_id=profile, skil=skill, rating=rating).save()
            if form6.is_valid():
                d = form6.cleaned_data.get('department')
                print(d)
                if d != "":
                    print("after d is not none")
                    try:
                        cep = Candidate_expdetail.objects.get(user_id=profile)
                    except Candidate_profile.DoesNotExist:
                        cep = None
                    if cep:
                        cep.delete()
                    f6 = form6.save(commit=False)
                    f6.user_id = profile
                    f6.save()
            if form7.is_valid():
                f7 = form7.save(commit=False)
                f7.user_id = profile
                f7.save()
            if form8.is_valid():
                for form in form8:

                    skill = form.cleaned_data.get('skill')
                    rating =form.cleaned_data.get('rating')

                    if skill:
                        Candidate_skills(user_id=profile, skill=skill,rating=rating).save()
            return redirect('jobseeker:ProfileEdit')
        print(request.method)
        try:
            c = Candidate_profile.objects.get(user_id=profile)
            print(c)
        except Candidate_profile.DoesNotExist:
            c = None
            print(c)
        try:
            cr = Candidate_resume.objects.get(user_id=profile)
        except Candidate_resume.DoesNotExist:
            cr = None
        if cr is not None:
            re = True
        else:
            re = False
        try:
            cep = Candidate_expdetail.objects.get(user_id=profile)
        except Candidate_expdetail.DoesNotExist:
            cep = None
        try:
            Resume = Resume_headline.objects.get(user_id = profile)
        except Resume_headline.DoesNotExist:
            Resume = None

        form1 = ProfileRegisterForm(instance=c)
        form2 = ProfileRegisterForm_edu()
        form3 = ProfileRegisterForm_profdetail()
        form4 = ProfileRegisterForm_resume(instance=cr)

        form6 = ProfileRegistration_expdetail(instance=cep)
        form7 = Resume_headlineForm(instance=Resume)
        form8=ProfileRegistration_skills()
        skills = Candidate_skills.objects.filter(user_id=profile)
        print(skills)
        edu = Candidate_edu.objects.filter(user_id=profile)
        professional = Candidate_profdetail.objects.filter(user_id=profile)
        return render(request, 'jobseeker/Profile.html',
                      {"form1": form1, 'form2': form2, "form3": form3, 'form4': form4, 'form6': form6,'form7':form7,'form8':form8,
                       'skills': skills, 'edu': edu, 'professional': professional, 'c': c,'cr':cr,'re':re,'rh':Resume})

    else:
        return redirect('/')


@login_required(login_url='/')
def create_profile(request):
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

            # f5 = form5.save(commit=False)
            # f5.user_id = profile
            # f5.save()
            for form in form5:
                # extract name from each form and save
                skill = form.cleaned_data.get('skill')
                rating = form.cleaned_data.get('rating')
                # save book instance
                if skill:
                    Candidate_skills(user_id=profile, skil=skill, rating=rating).save()

            f6 = form6.save(commit=False)
            f6.user_id = profile
            f6.save()
            return redirect('jobseeker:jobseeker_home')

    form1 = ProfileRegisterForm()
    form2 = ProfileRegisterForm_edu()
    form3 = ProfileRegisterForm_profdetail()
    form4 = ProfileRegisterForm_resume()
    form5 = ProfileRegistration_skills()
    form6 = ProfileRegistration_expdetail()

    return render(request, 'jobseeker/createprofile.html',
                  {"form1": form1, 'form2': form2, "form3": form3, 'form4': form4, "form5": form5, 'form6': form6})


@login_required(login_url='/')
def SavedJobs(request):
    if request.method == 'GET':
        val = request.GET.get('search_box', None)
        print("val")
        print(val)
        if val:
            job = Employer_job.objects.filter(
                Q(job_title__icontains=val) |
                Q(skill__icontains=val) |
                Q(job_description__icontains=val) |
                Q(job_salary__icontains=val) |
                Q(job_location__icontains=val)
            ).distinct()
            print(job)
            jobs = []
            job_ques = []
            relevant_jobs = []
            common = []
            companyprofile = []
            job_skills = []
            u = request.user
            if u is not None and u.is_candidate:
                c = Candidate.objects.get(user=u)
                try:
                    cp = Candidate_profile.objects.get(user_id=c)
                except Candidate_profile.DoesNotExist:
                    cp = None
                try:
                    cep = Candidate_expdetail.objects.get(user_id=c)
                except Candidate_expdetail.DoesNotExist:
                    cep = None
                try:
                    cr = Candidate_resume.objects.get(user_id=c)
                except Candidate_resume.DoesNotExist:
                    cr = None
                if u.first_login:

                    skills = Candidate_skills.objects.filter(user_id=c)
                    print("skills")
                    print(skills)
                    if len(skills) != 0:

                        my_sk = []
                        j = 0
                        for i in skills:
                            my_sk.insert(j, i.skill.lower())
                            j = j + 1

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
                        pj = Paginator(relevant_jobs, 5)
                        pjt = Paginator(relevant_jobs, 5)
                        pc = Paginator(common, 5)
                        pjs = Paginator(job_skills, 5)
                        pjq = Paginator(job_ques, 5)
                        pcp = Paginator(companyprofile, 5)
                        page_num = request.GET.get('page', 1)
                        try:
                            pj_objects = pj.page(page_num)
                            pjt_objects = pjt.page(page_num)
                            pc_objects = pc.page(page_num)
                            pjs_objects = pjs.page(page_num)
                            pjq_objects = pjq.page(page_num)
                            pcp_objects = pcp.page(page_num)
                        except EmptyPage:
                            pj_objects = pj.page(1)
                            pjt_objects = pjt.page(1)
                            pc_objects = pc.page(1)
                            pjs_objects = pjs.page(1)
                            pjq_objects = pjq.page(1)
                            pcp_objects = pcp.page(1)
                        objects = zip(pj_objects, pc_objects, pjs_objects, pjq_objects, pcp_objects)

                        return render(request, 'jobseeker/home.html',
                                      {'jobs': objects, 'c': c, 'cp': cp, 'cep': cep, 'cr': cr, 'pjs': pjt_objects})
                        # objects = zip(relevant_jobs, common, job_skills, job_ques, companyprofile)
                        #
                        # return render(request, 'jobseeker/home.html',
                        #               {'jobs': objects, 'c': c, 'cp': cp, 'cep': cep, 'cr': cr})
                    else:

                        print("len job")
                        print(len(job))
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
                            # print(diff)
                            if diff > 30:
                                # expired_job.append(j)
                                Employer_expired_job.objects.create(job_id=j).save()

                            else:
                                jobs.append(j)
                            print("len")
                            print(len(jobs))
                        for jo in jobs:
                            skills = []
                            sk = str(jo.skill).split(",")
                            for i in sk:
                                skills.append(i.strip().lower())
                            common_skill = []
                            e = jo.employer_id
                            companyprofile.append(Employer_profile.objects.get(employer=e))
                            try:
                                userS = Employer_job_Saved.objects.get(job_id=jo.pk, candidate_id=c)
                                # print(userS.job_id)
                            except Employer_job_Saved.DoesNotExist:
                                userS = None
                            try:
                                userA = Employer_job_Applied.objects.get(job_id=jo.pk, candidate_id=c)
                                # print(userA.job_id)
                            except Employer_job_Applied.DoesNotExist:
                                userA = None

                            if userA:
                                # print(userA)
                                continue
                            if userS:
                                # print(userS)
                                continue
                            relevant_jobs.append(jo)

                            common.append(len(common_skill))
                            job_skills.append(len(skills))
                            job_ques.append(Employer_jobquestion.objects.filter(job_id=jo))
                        pj = Paginator(relevant_jobs, 5)
                        pjt = Paginator(relevant_jobs, 5)
                        pc = Paginator(common, 5)
                        pjs = Paginator(job_skills, 5)
                        pjq = Paginator(job_ques, 5)
                        pcp = Paginator(companyprofile, 5)
                        page_num = request.GET.get('page', 1)
                        try:
                            pj_objects = pj.page(page_num)
                            pjt_objects = pjt.page(page_num)
                            pc_objects = pc.page(page_num)
                            pjs_objects = pjs.page(page_num)
                            pjq_objects = pjq.page(page_num)
                            pcp_objects = pcp.page(page_num)
                        except EmptyPage:
                            pj_objects = pj.page(1)
                            pjt_objects = pjt.page(1)
                            pc_objects = pc.page(1)
                            pjs_objects = pjs.page(1)
                            pjq_objects = pjq.page(1)
                            pcp_objects = pcp.page(1)
                        objects = zip(pj_objects, pc_objects, pjs_objects, pjq_objects, pcp_objects)

                        return render(request, 'jobseeker/home.html',
                                      {'jobs': objects, 'c': c, 'cp': cp, 'cep': cep, 'cr': cr, 'pjs': pjt_objects})

        else:
            job_ques = []
            companyprofile = []
            relevant_jobs = []
            common = []
            job_skills = []
            my_sk = []
            post_date = []
            saved_date = []
            user = request.user
            if user is not None and user.is_candidate:
                c = Candidate.objects.get(user=request.user)
                try:
                    cp = Candidate_profile.objects.get(user_id=c)
                except Candidate_profile.DoesNotExist:
                    cp = None
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
                                post_date.append(job.created_on)
                                saved_date.append(userS.saved_on)
                                companyprofile.append(Employer_profile.objects.get(employer=e))
                                # print(userS)
                                # continue
                                relevant_jobs.append(job)
                                common.append(len(common_skills))
                                job_skills.append(len(skills))
                                job_ques.append(Employer_jobquestion.objects.filter(job_id=job))

                    pj = Paginator(relevant_jobs, 1)
                    pjt = Paginator(relevant_jobs, 1)
                    pc = Paginator(common, 1)
                    pjs = Paginator(job_skills, 1)
                    pjq = Paginator(job_ques, 1)
                    pcp = Paginator(companyprofile, 1)
                    page_num = request.GET.get('page', 1)
                    try:
                        pj_objects = pj.page(page_num)
                        pjt_objects = pjt.page(page_num)
                        pc_objects = pc.page(page_num)
                        pjs_objects = pjs.page(page_num)
                        pjq_objects = pjq.page(page_num)
                        pcp_objects = pcp.page(page_num)
                    except EmptyPage:
                        pj_objects = pj.page(1)
                        pjt_objects = pjt.page(1)
                        pc_objects = pc.page(1)
                        pjs_objects = pjs.page(1)
                        pjq_objects = pjq.page(1)
                        pcp_objects = pcp.page(1)
                    objects = zip(pj_objects, pc_objects, pjs_objects, pjq_objects, pcp_objects)

                    return render(request, 'jobseeker/savedjobs.html',
                                  {'jobs': objects, 'c': c, 'cp': cp, 'pjs': pjt_objects})

                else:
                    return render(request, 'jobseeker/savedjobs.html', {'cp': cp})
            else:
                return redirect('/')
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


@login_required(login_url='/')
def AppliedJobs(request):
    if request.method == 'GET':
        val = request.GET.get('search_box', None)
        print("val")
        print(val)
        if val:
            job = Employer_job.objects.filter(
                Q(job_title__icontains=val) |
                Q(skill__icontains=val) |
                Q(job_description__icontains=val) |
                Q(job_salary__icontains=val) |
                Q(job_location__icontains=val)
            ).distinct()
            print(job)
            jobs = []
            job_ques = []
            relevant_jobs = []
            common = []
            companyprofile = []
            job_skills = []
            u = request.user
            if u is not None and u.is_candidate:
                c = Candidate.objects.get(user=u)
                try:
                    cp = Candidate_profile.objects.get(user_id=c)
                except Candidate_profile.DoesNotExist:
                    cp = None
                try:
                    cep = Candidate_expdetail.objects.get(user_id=c)
                except Candidate_expdetail.DoesNotExist:
                    cep = None
                try:
                    cr = Candidate_resume.objects.get(user_id=c)
                except Candidate_resume.DoesNotExist:
                    cr = None
                if u.first_login:

                    skills = Candidate_skills.objects.filter(user_id=c)
                    print("skills")
                    print(skills)
                    if len(skills) != 0:

                        my_sk = []
                        j = 0
                        for i in skills:
                            my_sk.insert(j, i.skill.lower())
                            j = j + 1

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

                        pj = Paginator(relevant_jobs, 5)
                        pjt = Paginator(relevant_jobs, 5)
                        pc = Paginator(common, 5)
                        pjs = Paginator(job_skills, 5)
                        pjq = Paginator(job_ques, 5)
                        pcp = Paginator(companyprofile, 5)
                        page_num = request.GET.get('page', 1)
                        try:
                            pj_objects = pj.page(page_num)
                            pjt_objects = pjt.page(page_num)
                            pc_objects = pc.page(page_num)
                            pjs_objects = pjs.page(page_num)
                            pjq_objects = pjq.page(page_num)
                            pcp_objects = pcp.page(page_num)
                        except EmptyPage:
                            pj_objects = pj.page(1)
                            pjt_objects = pjt.page(1)
                            pc_objects = pc.page(1)
                            pjs_objects = pjs.page(1)
                            pjq_objects = pjq.page(1)
                            pcp_objects = pcp.page(1)
                        objects = zip(pj_objects, pc_objects, pjs_objects, pjq_objects, pcp_objects)

                        return render(request, 'jobseeker/home.html',
                                      {'jobs': objects, 'c': c, 'cp': cp, 'cep': cep, 'cr': cr, 'pjs': pjt_objects})
                    else:

                        print("len job")
                        print(len(job))
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
                            # print(diff)
                            if diff > 30:
                                # expired_job.append(j)
                                Employer_expired_job.objects.create(job_id=j).save()

                            else:
                                jobs.append(j)
                            print("len")
                            print(len(jobs))
                        for jo in jobs:
                            skills = []
                            sk = str(jo.skill).split(",")
                            for i in sk:
                                skills.append(i.strip().lower())
                            common_skill = []
                            e = jo.employer_id
                            companyprofile.append(Employer_profile.objects.get(employer=e))
                            try:
                                userS = Employer_job_Saved.objects.get(job_id=jo.pk, candidate_id=c)
                                # print(userS.job_id)
                            except Employer_job_Saved.DoesNotExist:
                                userS = None
                            try:
                                userA = Employer_job_Applied.objects.get(job_id=jo.pk, candidate_id=c)
                                # print(userA.job_id)
                            except Employer_job_Applied.DoesNotExist:
                                userA = None

                            if userA:
                                # print(userA)
                                continue
                            if userS:
                                # print(userS)
                                continue
                            relevant_jobs.append(jo)
                            print("job:")
                            print(jo)

                            common.append(len(common_skill))
                            job_skills.append(len(skills))
                            job_ques.append(Employer_jobquestion.objects.filter(job_id=jo))
                        pj = Paginator(relevant_jobs, 5)
                        pjt = Paginator(relevant_jobs, 5)
                        pc = Paginator(common, 5)
                        pjs = Paginator(job_skills, 5)
                        pjq = Paginator(job_ques, 5)
                        pcp = Paginator(companyprofile, 5)
                        page_num = request.GET.get('page', 1)
                        try:
                            pj_objects = pj.page(page_num)
                            pjt_objects = pjt.page(page_num)
                            pc_objects = pc.page(page_num)
                            pjs_objects = pjs.page(page_num)
                            pjq_objects = pjq.page(page_num)
                            pcp_objects = pcp.page(page_num)
                        except EmptyPage:
                            pj_objects = pj.page(1)
                            pjt_objects = pjt.page(1)
                            pc_objects = pc.page(1)
                            pjs_objects = pjs.page(1)
                            pjq_objects = pjq.page(1)
                            pcp_objects = pcp.page(1)
                        objects = zip(pj_objects, pc_objects, pjs_objects, pjq_objects, pcp_objects)

                        return render(request, 'jobseeker/home.html',
                                      {'jobs': objects, 'c': c, 'cp': cp, 'cep': cep, 'cr': cr, 'pjs': pjt_objects})
        else:
            companyprofile = []
            user = request.user
            if user is not None and user.is_candidate:
                c = Candidate.objects.get(user=request.user)
                try:
                    cp = Candidate_profile.objects.get(user_id=c)
                except Candidate_profile.DoesNotExist:
                    cp = None
                applied = Employer_job_Applied.objects.filter(candidate_id=c)
                for a in applied:
                    e = a.job_id.employer_id
                    companyprofile.append(Employer_profile.objects.get(employer=e))

                pj = Paginator(applied, 5)
                pjt = Paginator(applied, 5)
                pc = Paginator(companyprofile, 5)
                # pjs = Paginator(job_skills, 5)
                # pjq = Paginator(job_ques, 5)
                # pcp = Paginator(companyprofile, 5)
                page_num = request.GET.get('page', 1)
                try:
                    pj_objects = pj.page(page_num)
                    pjt_objects = pjt.page(page_num)
                    pc_objects = pc.page(page_num)
                    # pjs_objects = pjs.page(page_num)
                    # pjq_objects = pjq.page(page_num)
                    # pcp_objects = pcp.page(page_num)
                except EmptyPage:
                    pj_objects = pj.page(1)
                    pjt_objects = pjt.page(1)
                    pc_objects = pc.page(1)
                    # pjs_objects = pjs.page(1)
                    # pjq_objects = pjq.page(1)
                    # pcp_objects = pcp.page(1)
                objects = zip(pj_objects, pc_objects)

                return render(request, 'jobseeker/applied.html',
                              {'jobs': objects, 'c': c, 'cp': cp, 'pjs': pjt_objects})
                # objects = zip(applied, companyprofile)
                # return render(request, 'jobseeker/applied.html', {'jobs': objects, 'cp': cp})
            else:
                return redirect('/')


@login_required(login_url='/')
def remove_applied(request, pk):
    Employer_job_Applied.objects.get(pk=pk).delete()

    return redirect('jobseeker:AppliedJobs')


@login_required(login_url='/')
def remove_saved(request, pk):
    c = Candidate.objects.get(user=request.user)
    job = Employer_job.objects.get(pk=pk)
    savej = Employer_job_Saved.objects.filter(job_id=job)
    for s in savej:
        if s.candidate_id == c:
            s.delete()

    return redirect('jobseeker:SavedJobs')


def ResumeCreation(request):
    if request.method == 'GET':
        form1 = Resumeforming_Entery(request.GET or None)
        form2 = Resumeforming_Mid(request.GET or None)
        form3 = Resumeforming_senior(request.GET or None)
        form4 = Resumeforming_Executive(request.GET or None)

    elif request.method == 'POST':
        print(request.POST)
        form1 = Resumeforming_Entery(request.POST)
        form2 = Resumeforming_Mid(request.POST)
        form3 = Resumeforming_senior(request.POST)
        form4 = Resumeforming_Executive(request.POST)

        if form1.is_valid():

            # f = form1.save(commit=False)
            selected = form1.cleaned_data.get("delivery_type")
            print(selected)
            if selected:
                Experience = "a"
                if selected == "Regular 8 working days":
                    add = 0
                elif selected == "Express 4 working days(1250/-)":
                    add = 1250
                elif selected == "Super Express 2 working days(2300)":
                    add = 2300

                return redirect('jobseeker:resume_payment', Experience, add)
                #
                # f.candidate = c
                # if f.resume_type == 'A':
                #     f.amount = 250
                # elif f.resume_type == 'B':
                #     f.amount = 250
                # elif f.resume_type == 'C':
                #     f.amount = 250
                #
                # f.save()
                # pk = f.pk

                # return redirect('jobseeker:resume_payment', pk)
        elif form2.is_valid():

            # f = form2.save(commit=False)
            selected = form2.cleaned_data.get("delivery_type_Mid")
            print(selected)
            if selected:
                Experience = "b"
                if selected == "Regular 8 working days":
                    add = 0
                elif selected == "Express 4 working days(1250/-)":
                    add = 1250
                elif selected == "Super Express 2 working days(2300)":
                    add = 2300

                return redirect('jobseeker:resume_payment', Experience, add)
                # f.candidate = c
                # if f.resume_type == 'A':
                #     f.amount = 250
                # elif f.resume_type == 'B':
                #     f.amount = 250
                # elif f.resume_type == 'C':
                #     f.amount = 250
                #
                # f.save()
                # pk = f.pk
                #
                # return redirect('jobseeker:resume_payment', pk)
        elif form3.is_valid():

            # f = form3.save(commit=False)
            selected = form3.cleaned_data.get("delivery_type_senior")
            print(selected)
            if selected:
                Experience = "c"
                if selected == "Regular 8 working days":
                    add = 0
                elif selected == "Express 4 working days(1250/-)":
                    add = 1250
                elif selected == "Super Express 2 working days(2300)":
                    add = 2300

                return redirect('jobseeker:resume_payment', Experience, add)
                # f.candidate = c
                #
                # if f.resume_type == 'A':
                #     f.amount = 250
                # elif f.resume_type == 'B':
                #     f.amount = 250
                # elif f.resume_type == 'C':
                #     f.amount = 250
                #
                # f.save()
                # pk = f.pk
                #
                # return redirect('jobseeker:resume_payment', pk)
        elif form4.is_valid():

            # f = form4.save(commit=False)
            selected = form4.cleaned_data.get("delivery_type_Executive")
            print(selected)
            if selected:
                # print("form4:")
                # print(form4)
                # f.candidate = c
                # if f.resume_type == 'A':
                #     f.amount = 250
                # elif f.resume_type == 'B':
                #     f.amount = 250
                # elif f.resume_type == 'C':
                #     f.amount = 250
                #
                # f.save()
                # pk = f.pk
                #
                Experience = "d"
                if selected == "Regular 8 working days":
                    add = 0
                elif selected == "Express 4 working days(1250/-)":
                    add = 1250
                elif selected == "Super Express 2 working days(2300)":
                    add = 2300

                return redirect('jobseeker:resume_payment', Experience, add)

    return render(request, 'jobseeker/resume.html', {'form1': form1, 'form2': form2, 'form3': form3, 'form4': form4})


@login_required(login_url='/')
def payment(request, Experience, add):
    c = Candidate.objects.get(user=request.user)
    print("paymentgateway:")
    print(Experience)
    print(add)
    if add == 0:
        delivery_type = "Regular 8 working days"
    if add == 1250:
        delivery_type = "Express 4 working days(1250/-)"
    if add == 2300:
        delivery_type = "Super Express 2 working days(2300)"

    if Experience == "a":
        exp = "0-3"
        Payment = 2500 + add
    if Experience == "b":
        exp = "3-8"
        Payment = 1500 + add
    if Experience == "c":
        exp = "8-15"
        Payment = 3500 + add
    if Experience == "d":
        exp = "15+"
        Payment = 4500 + add
    r = Resume_order.objects.create(candidate=c, year_experience=exp, delivery_type=delivery_type, amount=Payment)
    # r = Resume_order.objects.get(pk=pk)
    a = Payment * 100
    print(a)
    name = r.candidate.user
    print(r)
    if request.method == 'POST':
        order_amount = a
        order_currency = 'INR'

        payment = client.order.create(amount=order_amount, currency=order_currency)
        r.is_payment_Done = True
        r.save()
        print(r)
        return redirect('jobseeker:jobseeker_home')
    return render(request, 'jobseeker/payment.html', {'amount': a, 'user': name})


def BuiltResume(request):
    if request.method=='POST':
        name = request.GET.get('name', None)
        mname = request.GET.get('middlename', None)
        lname = request.GET.get('lastname', None)
        dob = request.GET.get('dob', None)
        gender = request.GET.get('gender', None)
        marital_status = request.GET.get('marital_status', None)
        email = request.GET.get('email', None)
        mobile = request.GET.get('mobile', None)
        address = request.GET.get('address', None)
        city = request.GET.get('city', None)
        state = request.GET.get('state', None)
        pin = request.GET.get('pin', None)
        url = request.GET.get('search_box', None)
        img = request.FILES['image']





    return render(request, 'jobseeker/BuiltResume.html')
