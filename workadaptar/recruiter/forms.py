from django import forms
from django.contrib.auth.forms import UserCreationForm
from user_custom.models import User_custom
from .models import Employer_profile, Employer_job, Employer_jobquestion
from django.forms import formset_factory

experience = [
    ('1-3', '1-3'),
    ('4-7', '4-7'),
    ('8+', '8+'),
]
job_Type = [
    ('Part time', 'Part time'),
    ('Full time', 'Full time'),
    ('Internship', 'Internship'),
]
class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Enter your first name', 'class': "input100"}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Enter your last name', 'class': "input100"}))
    email = forms.EmailField(max_length=254,
                             widget=forms.TextInput(attrs={'placeholder': 'Enter email address', 'class': "input100"}))
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter Password ', 'class': "input100"}))
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(
        attrs={'placeholder': 'cConfirm Password ', 'class': "input100"}))

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
    job_title = forms.CharField(max_length=50,label='Job Title', required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Enter your Job Title', 'class': "input100"}))
    job_description = forms.CharField(max_length=1500, label='job description', required=False, widget=forms.Textarea(
        attrs={'placeholder': 'Enter your Job description', 'class': "input100"}))
    employment_type = forms.ChoiceField(choices=job_Type, required=False, label='employment type', widget=forms.Select(
        attrs={ 'class': "input100"}))
    job_location = forms.CharField(max_length=100, label='job location', required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Enter your job location', 'class': "input100"}))
    job_experience = forms.ChoiceField(choices=experience, required=False, label='job experience', widget=forms.Select(
        attrs={'class': "input100"}))
    skill = forms.CharField(max_length=50, label='skill', required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Enter your skill', 'class': "input100"}))

    class Meta:
        model = Employer_job
        fields = [
            'job_title',
            'job_description',
            'employment_type',
            'job_location',
            'job_experience',
            'skill',

        ]


class JobsQuestionForm(forms.Form):
    question = forms.CharField(
        label='Question',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter Question here'
        })
    )
    # answer_size =forms.IntegerField(label='size of answer',
    #     widget=forms.TextInput(attrs={
    #         'class': 'form-control',
    #         'placeholder': 'Enter maxlength of answer by the candidate'
    #     }))


QuestionFormset = formset_factory(JobsQuestionForm, extra=1)
