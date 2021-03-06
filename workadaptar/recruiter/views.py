import re

import requests
from django.http import HttpResponse, JsonResponse
from django.db.models import Q
from django.utils.http import urlsafe_base64_decode
from user_custom.models import User_custom
from django.utils.encoding import force_text
from .models import Employer, Employer_profile, Employer_candidate_jobanswer, Employer_job, Employer_job_Applied, \
    Employer_jobquestion, Employer_expired_job, Employer_Subscription
from .forms import SignUpForm, ProfileRegisterForm, JobPostForm, JobsQuestionForm, QuestionFormset, keyWordFormset
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
    Candidate_expdetail, Candidate
from datetime import datetime
from django.forms import modelformset_factory
from django.db import transaction, IntegrityError
from django.contrib.auth.decorators import login_required
from bs4 import BeautifulSoup
import razorpay
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from django.http import HttpResponseBadRequest

headers = {
    'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
razorpay_client = razorpay.Client(
    auth=(settings.RAZOR_KEY_ID, settings.RAZOR_KEY_SECRET))


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
                user.is_active = True
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
                user.email_user(subject, message)
                messages.success(
                    request, ('Please check your mail for complete registration.'))
                return redirect('recruiter:employer/login')
                # username = form.cleaned_data['email']
                # password = form.cleaned_data['password1']
                #
                # # print(username)
                # # print(password)
                # user = authenticate(request, username=username, password=password)

                # if user is not None and user.is_employeer:
                #     login(request, user)
                #     return redirect('recruiter:employer_home')
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
            print(user)

        if user is not None and account_activation_token.check_token(user, token):
            user.is_active = True

            pr = Employer.objects.get(user=user)
            pr.is_email_verified = True
            pr.save()
            user.save()
            login(request, user)
            messages.success(request, ('Your account have been confirmed.'))
            return redirect('recruiter:employer_home')
        else:
            messages.warning(
                request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('recruiter:employer_home')


def login_employer(request):
    if request.user.is_authenticated and request.user.is_employeer:
        print(request.user)
        return redirect('recruiter:employer_home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('pass')
            Pattern = re.compile("(0|91)?[0-9]{10}")
            if Pattern.match(username):
                c = Employer_profile.objects.get(phone=username)
                username = c.user_id.user.username
            print(password)
            print(username)
            user = authenticate(request, username=username, password=password)
            print(user)

            if user is not None and user.is_employeer:
                login(request, user)
                if 'next' in request.POST:
                    return redirect(request.POST.get('next'))
                else:
                    return redirect('recruiter:employer_home')
            else:
                messages.info(request, 'Username OR password is incorrect')

        context = {}
        return render(request, 'index.html', context)
        # return render(request, 'employer/login.html', context)


@login_required(login_url='/')
def Home(request):
    jobs = []
    expired_job = []
    user = request.user
    if user is not None and user.is_employeer:
        if user.first_login:
            try:
                e = Employer.objects.get(user=user)
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
                return redirect('/')
        else:
            user.first_login = True
            user.save()
            return redirect('recruiter:job_post')
    else:
        return redirect('/')


@login_required(login_url='/')
def unpublish(request, pk):
    user = request.user
    job = Employer_job.objects.get(pk=pk)
    # print(c)
    # print(job)
    Employer_expired_job.objects.create(job_id=job).save()
    return redirect('recruiter:employer_home')


@login_required(login_url='/')
def remove_unpublish(request, pk):
    job = Employer_job.objects.get(pk=pk)
    unpub_job = Employer_expired_job.objects.get(job_id=job)
    unpub_job.delete()
    job.created_on = datetime.now()
    job.save()

    return redirect('recruiter:employer_home')


@login_required(login_url='/')
def edit_job(request, pk):
    user = request.user
    if user is not None and user.is_employeer:
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
    else:
        return redirect('/')


@login_required(login_url='/')
def job_detail(request, pk):
    user = request.user
    if user is not None and user.is_employeer:
        e = Employer.objects.get(user=request.user)
        job = Employer_job.objects.get(pk=pk)
        company = Employer_profile.objects.get(employer=e)
        # candidate_Applied = Employer_job_Applied.objects.filter(job_id=job)
        # objects = zip(job,candidate_Applied)
        return render(request, 'employer/job_details.html', {'job': job, 'c': company})
    else:
        return redirect('/')


@login_required(login_url='/')
def view_applied_candidate(request, pk):
    user = request.user
    if user is not None and user.is_employeer:
        e = Employer.objects.get(user=user)
        try:
            eS = Employer_Subscription.objects.get(emp_id=e)
        except Employer_Subscription.DoesNotExist:
            eS = None

        if eS is not None:
            start_date = eS.subscribed_on
            today = datetime.now()
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
            if diff > eS.subscription_interval:
                eS.delete()

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

            cp = Employer_profile.objects.get(employer=e)
            job = Employer_job.objects.get(pk=pk)

            valkey = request.GET.get('keyword_box', None)
            valcomp = request.GET.get('company_box', None)
            valloc = request.GET.get('location_box', None)
            valmin_box = request.GET.get('min_box', None)
            valmax_box = request.GET.get('max_box', None)
            valmin_salary_box = request.GET.get('min_salary_box', None)
            valmax_salary_box = request.GET.get('max_salary_box', None)
            question = Employer_jobquestion.objects.filter(job_id=job)
            candidate_Applied = Employer_job_Applied.objects.filter(job_id=job)
            for can in candidate_Applied:
                c = can.candidate_id
                c_p = Candidate_profile.objects.get(user_id=c)
                c_e = Candidate_edu.objects.filter(user_id=c).first()
                p_p = Candidate_profdetail.objects.filter(user_id=c)
                c_ed = Candidate_expdetail.objects.get(user_id=c)
                c_sk = Candidate_skills.objects.filter(user_id=c)
                if (valkey is not None) | (valloc is not None) | (valcomp is not None) | (valmax_box is not None) | (
                        valmin_box is not None) | (
                        valmin_box is not None) | (valmax_salary_box is not None) | (valmin_salary_box is not None):
                    for c_sks in c_sk:
                        try:
                            c_skss = c_sks.skill
                        except c_sks.DoesNotExist:
                            pass
                        if c_skss == valkey:

                            candidate_profile.append(c_p)
                            print("working filter")
                            print(candidate_profile)
                            candidate_user.append(c.user)
                            education_profile.append(c_e)
                            professional_profile.append(p_p)
                            expect.append(c_ed)
                            skill.append(c_sk)

                            resume.append(Candidate_resume.objects.get(user_id=c))
                            for q in question:
                                candidate_answer.append(
                                    Employer_candidate_jobanswer.objects.get(question_id=q, candidate_id=c))
                            continue
                        else:
                            pass

                    if valloc in c_ed.prefer_location:
                        print(valloc)

                        candidate_profile.append(c_p)
                        print("working location filter")
                        print(candidate_profile)
                        candidate_user.append(c.user)
                        education_profile.append(c_e)
                        professional_profile.append(p_p)
                        expect.append(c_ed)
                        skill.append(c_sk)

                        resume.append(Candidate_resume.objects.get(user_id=c))
                        for q in question:
                            candidate_answer.append(
                                Employer_candidate_jobanswer.objects.get(question_id=q, candidate_id=c))
                        continue
                    for p_ps in p_p:
                        try:
                            p_pss = p_ps.organization
                        except c_sks.DoesNotExist:
                            pass
                        if p_pss == valcomp:

                            candidate_profile.append(c_p)
                            print("working filter")
                            print(candidate_profile)
                            candidate_user.append(c.user)
                            education_profile.append(c_e)
                            professional_profile.append(p_p)
                            expect.append(c_ed)
                            skill.append(c_sk)

                            resume.append(Candidate_resume.objects.get(user_id=c))
                            for q in question:
                                candidate_answer.append(
                                    Employer_candidate_jobanswer.objects.get(question_id=q, candidate_id=c))
                            continue
                        else:
                            pass
                    if valmin_box <= c_ed.Total_Working <= valmax_box:

                        candidate_profile.append(c_p)
                        print("working location filter")
                        print(candidate_profile)
                        candidate_user.append(c.user)
                        education_profile.append(c_e)
                        professional_profile.append(p_p)
                        expect.append(c_ed)
                        skill.append(c_sk)

                        resume.append(Candidate_resume.objects.get(user_id=c))
                        for q in question:
                            candidate_answer.append(
                                Employer_candidate_jobanswer.objects.get(question_id=q, candidate_id=c))
                        continue
                    if valmin_salary_box <= c_ed.exp_salary <= valmax_salary_box:

                        candidate_profile.append(c_p)
                        print("working location filter")
                        print(candidate_profile)
                        candidate_user.append(c.user)
                        education_profile.append(c_e)
                        professional_profile.append(p_p)
                        expect.append(c_ed)
                        skill.append(c_sk)

                        resume.append(Candidate_resume.objects.get(user_id=c))
                        for q in question:
                            candidate_answer.append(
                                Employer_candidate_jobanswer.objects.get(question_id=q, candidate_id=c))
                        continue


                    else:
                        pass
                else:
                    candidate_profile.append(c_p)
                    candidate_user.append(c.user)
                    education_profile.append(c_e)
                    professional_profile.append(p_p)
                    expect.append(c_ed)
                    skill.append(c_sk)

                    resume.append(Candidate_resume.objects.get(user_id=c))
                    for q in question:
                        candidate_answer.append(Employer_candidate_jobanswer.objects.get(question_id=q, candidate_id=c))

            quest = zip(question, candidate_answer)
            # print(candidate_answer)
            objects = zip(candidate_profile, education_profile, professional_profile, skill, resume,
                          candidate_user, candidate_Applied, expect)

            return render(request, 'employer/job_candidate.html',
                          {'candidate': objects, 'job': job, 'question': question, 'answer': candidate_answer,
                           'cp': cp})
        else:
            currency = 'INR'
            amount = 20000  # Rs. 200

            # Create a Razorpay Order
            razorpay_order = razorpay_client.order.create(dict(amount=amount,
                                                               currency=currency,
                                                               payment_capture='0'))

            # order id of newly created order.
            razorpay_order_id = razorpay_order['id']
            callback_url = 'recruiter:paymenthandler'

            # we need to pass these details to frontend.
            context = {}
            context['razorpay_order_id'] = razorpay_order_id
            context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
            context['razorpay_amount'] = amount
            context['currency'] = currency
            context['callback_url'] = callback_url
            return render(request, 'employer/buySubscription.html', context=context)

    else:
        return redirect('/')


@csrf_exempt
def paymenthandler(request):
    # only accept POST request.
    if request.method == "POST":
        try:

            # get the required parameters from post request.
            payment_id = request.POST.get('razorpay_payment_id', '')
            razorpay_order_id = request.POST.get('razorpay_order_id', '')
            signature = request.POST.get('razorpay_signature', '')
            params_dict = {
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }

            # verify the payment signature.
            result = razorpay_client.utility.verify_payment_signature(
                params_dict)
            if result is None:
                amount = 20000  # Rs. 200
                try:

                    # capture the payemt
                    razorpay_client.payment.capture(payment_id, amount)

                    # render success page on successful caputre of payment
                    return render(request, 'employer/paymentsuccess.html')
                except:

                    # if there is an error while capturing payment.
                    return render(request, 'employer/paymentfail.html')
            else:

                # if signature verification fails.
                return render(request, 'employer/paymentfail.html')
        except:

            # if we don't find the required parameters in POST data
            return HttpResponseBadRequest()
    else:
        # if other than POST request is made.
        return HttpResponseBadRequest()


@login_required(login_url='/')
def shortlistview_applied_candidate(request, pk):
    user = request.user
    if user is not None and user.is_employeer:
        e = Employer.objects.get(user=user)
        cp = Employer_profile.objects.get(employer=e)
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
                      {'candidate': objects, 'job': job, 'question': question, 'answer': candidate_answer, 'cp': cp})
    else:
        return redirect('/')


@login_required(login_url='/')
def disqualifyview_applied_candidate(request, pk):
    user = request.user
    if user is not None and user.is_employeer:
        e = Employer.objects.get(user=user)
        cp = Employer_profile.objects.get(employer=e)
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
                      {'candidate': objects, 'job': job, 'question': question, 'answer': candidate_answer, 'cp': cp})
    else:
        return redirect('/')


@login_required(login_url='/')
def shortlist(request, pk):
    e = Employer_job_Applied.objects.get(pk=pk)
    e.is_shortlisted = True
    e.is_disqualified = False
    e.save()
    print(e.job_id.pk)
    return redirect('recruiter:view_applied_candidate', e.job_id.pk)


@login_required(login_url='/')
def disqualify(request, pk):
    e = Employer_job_Applied.objects.get(pk=pk)
    e.is_shortlisted = False
    e.is_disqualified = True
    e.save()
    print(e.job_id.pk)
    return redirect('recruiter:view_applied_candidate', e.job_id.pk)


@login_required(login_url='/')
def delete_job(request, pk):
    Employer_job.objects.get(pk=pk).delete()

    return redirect('recruiter:employer_home')


@login_required(login_url='/')
def publish_job(request, pk):
    e = Employer_job.objects.get(pk=pk)
    e.is_save_later = False
    e.save()
    return redirect('recruiter:job_detail', pk)


@login_required(login_url='/')
def ProfileView(request):
    u = request.user
    e = Employer.objects.get(user=u)
    profile = Employer_profile.objects.get(employer=e)

    return render(request, 'employer/skills.html', {
        "user": u,
        "profile": profile,

    })


@login_required(login_url='/')
def ProfileEdit(request):
    try:
        profile = Employer.objects.get(user=request.user)
    except Candidate.DoesNotExist:
        profile = None
    print(profile)
    print('notrun', request.method)
    if profile is not None:
        if request.method == 'POST':
            print('run', request.method)
            form1 = ProfileRegisterForm(data=request.POST or None, files=request.FILES or None)

            if form1.is_valid():
                print(form1.cleaned_data.get('profile_pic'))
                if form1.cleaned_data.get('birth_date'):
                    f1 = form1.save(commit=False)
                    try:
                        c = Employer_profile.objects.get(employer=profile)
                    except Employer_profile.DoesNotExist:
                        c = None
                    if c:
                        c.delete()

                    f1.user_id = profile

                    f1.save()

            return redirect('jobseeker:ProfileEdit')
        print(request.method)
        try:
            c = Employer_profile.objects.get(employer=profile)
        except Employer_profile.DoesNotExist:
            c = None

        form1 = ProfileRegisterForm(instance=c)

        return render(request, 'jobseeker/Profile.html',
                      {"form1": form1, 'c': c})

    else:
        return redirect('/')


@login_required(login_url='/')
def job_post(request):
    user = request.user
    if user is not None and user.is_employeer:
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

                    quest = form.cleaned_data.get('question')
                    # ans =form.cleaned_data.get('answer_size')

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
    else:
        return redirect('/')


@login_required(login_url='/')
def job_Response(request, pk):
    user = request.user
    if user is not None and user.is_employeer:
        job = Employer_job.objects.get(pk=pk)
        response = Employer_job_Applied.objects.filter(job_id=job)
        return render(request, 'dashboard/jobresponse.html', {'response': response})
    else:
        return redirect('/')


@login_required(login_url='/recruiter/login')
def advance_Search(request):
    user = request.user
    if user is not None and user.is_employeer:
        candidate_user = []
        candidate_profile = []
        education_profile = []
        professional_profile = []

        c_jobtitle = []
        c_location = []
        c_exp = []
        c_jobtype = []
        print(request.method)
        if request.method == 'GET':
            formset = keyWordFormset(request.GET or None)
        elif request.method == 'POST':
            print(request.POST)
            job_title = request.POST.get('job_title', None)
            location = request.POST.get('location', None)
            experience = request.POST.get('experience', None)
            job_type = request.POST.get('job_type', None)
            minExp = request.POST.get('minExp', None)
            maxExp = request.POST.get('maxExp', None)
            minlakh = request.POST.get('minlakh', None)
            minthousand = request.POST.get('minthousand', None)
            maxlakh = request.POST.get('maxlakh', None)
            maxthousand = request.POST.get('maxthousand', None)
            active = request.POST.get('active', None)

            formset = keyWordFormset(request.POST)
            if formset.is_valid():

                for form in formset:
                    keyword = form.cleaned_data.get('keyword')
                    print(keyword)
            if job_type == 'Job Type':
                job_type = None
            if experience == 'Experience':
                experience = None
            if location == 'Location':
                location = None
            if minExp == 'Minimum':
                minExp = None
            if maxExp == 'To Maximum':
                maxExp = None
            if minlakh == 'Lacs':
                minlakh = None
            if maxlakh == 'Lacs':
                maxlakh = None
            if minthousand == 'Thousand':
                minthousand = None
            if maxthousand == 'Thousand':
                maxthousand = None
            print(job_type)
            print(experience)
            print(location)
            candidates = Candidate.objects.all()

            for c in candidates:
                if (job_title is not None):
                    a = Candidate_expdetail.objects.filter(department=job_title)
                    for ab in a:
                        c_jobtitle.append(ab.user_id)
                else:
                    a = Candidate_expdetail.objects.all()
                    for ab in a:
                        c_jobtitle.append(ab.user_id)
                if (job_type is not None):
                    a = Candidate_expdetail.objects.filter(job_type=job_type)
                    for ab in a:
                        c_jobtype.append(ab.user_id)
                else:
                    a = Candidate_expdetail.objects.all()
                    for ab in a:
                        c_jobtitle.append(ab.user_id)
                if (experience is not None):
                    a = Candidate_expdetail.objects.filter(Total_Working=experience)
                    for ab in a:
                        c_jobtitle.append(ab.user_id)
                else:
                    a = Candidate_expdetail.objects.all()
                    for ab in a:
                        c_jobtitle.append(ab.user_id)
                if (location is not None):
                    a = Candidate_expdetail.objects.filter(prefer_location=location)
                    for ab in a:
                        c_jobtitle.append(ab.user_id)
                else:
                    a = Candidate_expdetail.objects.all()
                    for ab in a:
                        c_jobtitle.append(ab.user_id)
            s1 = set(c_jobtype)
            s2 = set(c_location)
            s3 = set(c_exp)
            s4 = set(c_jobtype)
            set1 = s1.intersection(s2)
            set2 = set1.intersection(s3)
            candidate_list_Set = set2.intersection(s4)
            candidate_list = list(candidate_list_Set)
            return JsonResponse({"msg": "done"})

        return render(request, 'employer/advance-search.html', {'form2': formset})
    else:
        return redirect('recruiter:employer/login')
