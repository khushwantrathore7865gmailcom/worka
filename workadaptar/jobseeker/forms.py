from django import forms
from django.contrib.auth.forms import UserCreationForm
from user_custom.models import User_custom
from .models import Candidate_profile, Candidate_edu, Candidate_profdetail, Candidate_resume


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False)
    last_name = forms.CharField(max_length=30, required=False)
    email = forms.EmailField(max_length=254)

    class Meta:
        model = User_custom
        fields = [
            'username',
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
        model = Candidate_profile
        fields = [
            'birth_day',
            'gender',
            'state',
            'marital_status',
            'profile_pic',
        ]


class ProfileRegisterForm_edu(forms.ModelForm):
    class Meta:
        model = Candidate_edu
        fields = [
            'institute_name',
            'start_date',
            'end_date',
            'course_type',
            'degree',
        ]


class ProfileRegisterForm_resume(forms.ModelForm):
    class Meta:
        model = Candidate_resume
        fields = [
            'resume_link',
            'coverletter_text',
            'coverletter_link',
        ]


class ProfileRegisterForm_profdetail(forms.ModelForm):
    class Meta:
        model = Candidate_profdetail
        fields = [
            'designation',
            'organization',
            'salary',
            'start_date',
            'end_date',
        ]
