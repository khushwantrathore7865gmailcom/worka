from django import forms
from django.contrib.auth.forms import UserCreationForm
from user_custom.models import User_custom
from .models import Employer_profile,Employer_job,Employer_jobquestion


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User_custom
        fields = [
            'first_name',
            'last_name',
            'email',
            'password1',
            'password2',
        ]

    def clean_email(self):
        email = self.cleaned_data.get('email')
        username = self.cleaned_data.get('username')

        if email and User_custom.objects.filter(email=email).exclude(username=username).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email


class ProfileRegisterForm(forms.ModelForm):
    class Meta:
        model = Employer_profile
        fields = [
            'phone',
            'company_type',
            'company_name',
            'company_logo',
        ]

class JobPostForm(forms.ModelForm):
    class Meta:
        model = Employer_job
        fields = [
            'job_title',
            'job_description',
            'employment_type',
            'job_location',
            'job_experience',


        ]
class JobsQuestionForm(forms.ModelForm):
    class Meta:
        model = Employer_jobquestion
        fields = [
            'question'

        ]