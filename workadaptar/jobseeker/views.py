from django.http import HttpResponse
from django.utils.http import urlsafe_base64_decode
from user_custom.models import User_custom
from django.utils.encoding import force_text
from .models import Candidate,Candidate_profile
from jobseeker.forms import SignUpForm,ProfileRegisterForm,ProfileRegisterForm_edu,ProfileRegisterForm_profdetail,ProfileRegisterForm_resume
from django.views.generic import View
from django.contrib import messages
from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.template.loader import render_to_string
from django.contrib.auth import login
from django.shortcuts import render, redirect
from jobseeker.tokens import account_activation_token
from recruiter.models import Employer_job,Employer_jobquestion

class SignUpView(View):
    form_class = SignUpForm

    template_name = 'account/signup.html'

    @classmethod
    def ref(self, request, uid, *args, **kwargs):
        form = self.form_class()
        # link = request.GET.get('ref=', None)
        return render(request, self.template_name, {'form': form, 'uid': uid})

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
                user.is_active = False# Deactivate account till it is confirmed
                user.is_candidate=True
                user.save()
                new_candidate = Candidate(user=user,is_email_verified=False)
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
            return redirect('dashboard_home')
        else:
            messages.warning(
                request, ('The confirmation link was invalid, possibly because it has already been used.'))
            return redirect('dashboard_home')

def Home(request):
    c = Candidate.objects.get(user=request.user)
    if Candidate_profile.objects.get(user_id=c):
        job= Employer_job.objects.filter(is_saved=False, is_applied=False)
        return render(request,'home',{'jobs':job})
    else:
        return redirect('')

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


# @login_required(login_url='/login/')
def ProfileView(request, pk):
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

    return render(request, 'dashboard/my-profile.html', {"form1": form1, 'form2': form2,"form3": form3, 'form4': form4})

