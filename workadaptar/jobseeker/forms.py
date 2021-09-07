from django import forms
from django.contrib.auth.forms import UserCreationForm
from user_custom.models import User_custom
from .models import Candidate_profile, Candidate_edu, Candidate_profdetail, Candidate_resume, Candidate_skills, \
    Candidate_expdetail, Resume_order

from django.forms import modelformset_factory
from django.forms import formset_factory

experience = [
    ('1-3', '1-3'),
    ('4-7', '4-7'),
    ('8+', '8+'),
]
resume = [
    ('A', 'A'),
    ('B', 'B'),
    ('C', 'C'),
]
job_Type = [
    ('Part time', 'Part time'),
    ('Full time', 'Full time'),
    ('Internship', 'Internship'),
]
Gender = [
    ('Male', 'Male'),
    ('Female', 'Female'),
    ('Others', 'Others'),
]
state_choices = (("Andhra Pradesh", "Andhra Pradesh"), ("Arunachal Pradesh ", "Arunachal Pradesh "), ("Assam", "Assam"),
                 ("Bihar", "Bihar"), ("Chhattisgarh", "Chhattisgarh"), ("Goa", "Goa"), ("Gujarat", "Gujarat"),
                 ("Haryana", "Haryana"), ("Himachal Pradesh", "Himachal Pradesh"),
                 ("Jammu and Kashmir ", "Jammu and Kashmir "), ("Jharkhand", "Jharkhand"), ("Karnataka", "Karnataka"),
                 ("Kerala", "Kerala"), ("Madhya Pradesh", "Madhya Pradesh"), ("Maharashtra", "Maharashtra"),
                 ("Manipur", "Manipur"), ("Meghalaya", "Meghalaya"), ("Mizoram", "Mizoram"), ("Nagaland", "Nagaland"),
                 ("Odisha", "Odisha"), ("Punjab", "Punjab"), ("Rajasthan", "Rajasthan"), ("Sikkim", "Sikkim"),
                 ("Tamil Nadu", "Tamil Nadu"), ("Telangana", "Telangana"), ("Tripura", "Tripura"),
                 ("Uttar Pradesh", "Uttar Pradesh"), ("Uttarakhand", "Uttarakhand"), ("West Bengal", "West Bengal"),
                 ("Andaman and Nicobar Islands", "Andaman and Nicobar Islands"), ("Chandigarh", "Chandigarh"),
                 ("Dadra and Nagar Haveli", "Dadra and Nagar Haveli"), ("Daman and Diu", "Daman and Diu"),
                 ("Lakshadweep", "Lakshadweep"),
                 ("National Capital Territory of Delhi", "National Capital Territory of Delhi"),
                 ("Puducherry", "Puducherry"))
Martial_Status = [
    ('Single', 'Single'),
    ('Married ', 'Married'),
]


class SignUpForm(UserCreationForm):
    first_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Enter your first name', 'class': "input100"}))
    last_name = forms.CharField(max_length=30, required=False, widget=forms.TextInput(
        attrs={'placeholder': 'Enter your first name', 'class': "input100"}))
    email = forms.EmailField(max_length=254,
                             widget=forms.TextInput(attrs={'placeholder': 'Enter email address', 'class': "input100"}))
    password1 = forms.CharField(max_length=16, widget=forms.PasswordInput(
        attrs={'placeholder': 'Enter Password ', 'class': "input100"}))
    password2 = forms.CharField(max_length=16, widget=forms.PasswordInput(
        attrs={'placeholder': 'confirm Password ', 'class': "input100"}))

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
        # username = self.cleaned_data.get('username')

        if email and User_custom.objects.filter(email=email).exists():
            raise forms.ValidationError(u'Email addresses must be unique.')
        return email


class ProfileRegisterForm(forms.ModelForm):
    birth_date = forms.CharField(max_length=30, required=False, label='Birthdate', widget=forms.TextInput(
        attrs={'class': "input100"}))
    birth_month = forms.CharField(max_length=30, required=False, label='Birth month', widget=forms.TextInput(
        attrs={'class': "input100"}))
    birth_year = forms.CharField(max_length=30, required=False, label='Birth year', widget=forms.TextInput(
        attrs={'class': "input100"}))
    gender = forms.CharField(max_length=30, required=False, label='Gender', widget=forms.TextInput(
        attrs={'class': "input100"}))
    address = forms.CharField(max_length=30, required=False, label='Address', widget=forms.TextInput(
        attrs={'class': "input100"}))
    city = forms.CharField(max_length=30, required=False, label='City', widget=forms.TextInput(
        attrs={'class': "input100"}))
    state = forms.ChoiceField(choices=state_choices, required=False, label='state', widget=forms.Select(
        attrs={'class': "input100"}))
    marital_status = forms.ChoiceField(choices=Martial_Status, required=False, label='Marital Status',
                                       widget=forms.Select(
                                           attrs={'class': "input100"}))
    profile_pic = forms.ImageField(max_length=30, required=False, label='Profile picture', widget=forms.FileInput(
        attrs={'class': "input100"}))

    class Meta:
        model = Candidate_profile
        fields = [
            'profile_pic',
            'birth_date',
            'birth_month',
            'birth_year',
            'gender',
            'address',
            'city',
            'state',
            'marital_status',

        ]

#
# ProfileRegisterForm_edu = modelformset_factory(
#
#     Candidate_edu,
#     fields=('institute_name',
#             'start_date',
#             'start_month',
#             'start_year',
#             'end_date',
#             'end_month',
#             'end_year',
#             'course_type',
#             'degree',),
#     extra=1,
#     widgets={'institute_name': forms.TextInput(attrs={
#         'class': 'form-control',
#
#     }),
#         'start_date': forms.TextInput(attrs={
#             'class': 'form-control',
#
#         }),
#         'start_month': forms.TextInput(attrs={
#             'class': 'form-control',
#
#         }),
#         'start_year': forms.TextInput(attrs={
#             'class': 'form-control',
#
#         }),
#         'end_date': forms.TextInput(attrs={
#             'class': 'form-control',
#
#         }),
#         'end_month': forms.TextInput(attrs={
#             'class': 'form-control',
#
#         }),
#         'end_year': forms.TextInput(attrs={
#             'class': 'form-control',
#
#         }),
#         'course_type': forms.TextInput(attrs={
#             'class': 'form-control',
#
#         }),
#         'degree': forms.TextInput(attrs={
#             'class': 'form-control',
#
#         }),
#     })


class ProfileRegisterForm_edu(forms.ModelForm):
    institute_name = forms.CharField(max_length=30, required=False, label='institute name', widget=forms.TextInput(
        attrs={'class': "input100"}))

    course_type = forms.CharField(max_length=30, required=False, label='course type', widget=forms.TextInput(
        attrs={'class': "input100"}))
    degree = forms.CharField(max_length=30, required=False, label='degree', widget=forms.TextInput(
        attrs={'class': "input100"}))
    start_date = forms.CharField(max_length=30, required=False, label='start date', widget=forms.TextInput(
        attrs={'class': "input100"}))
    start_month = forms.CharField(max_length=30, required=False, label='start month', widget=forms.TextInput(
        attrs={'class': "input100"}))
    start_year = forms.CharField(max_length=30, required=False, label='start year', widget=forms.TextInput(
        attrs={'class': "input100"}))

    end_date = forms.CharField(max_length=30, required=False, label='end date', widget=forms.TextInput(
        attrs={'class': "input100"}))
    end_month = forms.CharField(max_length=30, required=False, label='end month', widget=forms.TextInput(
        attrs={'class': "input100"}))
    end_year = forms.CharField(max_length=30, required=False, label='end year', widget=forms.TextInput(
        attrs={'class': "input100"}))


    class Meta:
        model = Candidate_edu
        fields = [
            'institute_name',
            'start_date',
            'start_month',
            'start_year',
            'end_date',
            'end_month',
            'end_year',
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

#
# ProfileRegisterForm_profdetail = modelformset_factory(
#
#     Candidate_profdetail,
#     fields=('designation',
#             'organization',
#             'salary',
#             'start_date',
#             'start_month',
#             'start_year',
#             'is_current',
#             'end_date',
#             'end_month',
#             'end_year',),
#     extra=1,
#     widgets={'designation': forms.TextInput(attrs={
#         'class': 'input100',
#
#     }),
#         'organization': forms.TextInput(attrs={
#             'class': 'input100',
#
#         }),
#         'salary': forms.TextInput(attrs={
#             'class': 'input100',
#
#         }),
#         'start_date': forms.TextInput(attrs={
#             'class': 'input100',
#
#         }),
#         'start_month': forms.TextInput(attrs={
#             'class': 'input100',
#
#         }),
#         'start_year': forms.TextInput(attrs={
#             'class': 'input100',
#
#         }),
#         'is_current': forms.CheckboxInput(attrs={
#             'class': 'input100',
#
#         }),
#         'end_date': forms.TextInput(attrs={
#             'class': 'form-control',
#
#         }),
#         'end_month': forms.TextInput(attrs={
#             'class': 'form-control',
#
#         }),
#         'end_year': forms.TextInput(attrs={
#             'class': 'form-control',
#
#         }),
#     })


class ProfileRegisterForm_profdetail(forms.ModelForm):
    designation = forms.CharField(max_length=30, required=False, label='designation', widget=forms.TextInput(
        attrs={'class': "input100"}))
    organization = forms.CharField(max_length=30, required=False, label='organization', widget=forms.TextInput(
        attrs={'class': "input100"}))
    salary = forms.CharField(max_length=30, required=False, label='salary', widget=forms.TextInput(
        attrs={'class': "input100"}))
    start_date = forms.CharField(max_length=30, required=False, label='start date', widget=forms.TextInput(
        attrs={'class': "input100"}))
    start_month = forms.CharField(max_length=30, required=False, label='start month', widget=forms.TextInput(
        attrs={'class': "input100"}))
    start_year = forms.CharField(max_length=30, required=False, label='start year', widget=forms.TextInput(
        attrs={'class': "input100"}))
    is_current = forms.BooleanField(label='Currently working',widget=forms.CheckboxInput())
    end_date = forms.CharField(max_length=30, required=False, label='end date', widget=forms.TextInput(
        attrs={'class': "input100"}))
    end_month = forms.CharField(max_length=30, required=False, label='end month', widget=forms.TextInput(
        attrs={'class': "input100"}))
    end_year = forms.CharField(max_length=30, required=False, label='end year', widget=forms.TextInput(
        attrs={'class': "input100"}))
    class Meta:
        model = Candidate_profdetail
        fields = [
            'designation',
            'organization',
            'salary',
            'start_date',
            'start_month',
            'start_year',
            'is_current',
            'end_date',
            'end_month',
            'end_year',
        ]
#
#
# ProfileRegistration_skills = modelformset_factory(
#
#     Candidate_skills,
#     fields=('skill',
#             'rating',
#             ),
#     extra=1,
#     widgets={'skill': forms.TextInput(attrs={
#         'class': 'form-control',
#
#     }),
#         'rating': forms.TextInput(attrs={
#             'class': 'form-control',
#
#         }),
#
#     })
#
class BookForm(forms.Form):
    skill = forms.CharField(
        label='Skill',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter skill:'
        })
    )
    rating = forms.CharField(
        label='Rating',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter rating of skill:'
        })
    )


ProfileRegistration_skills = formset_factory(BookForm, extra=1)


# class ProfileRegistration_skills(forms.ModelForm):
#     class Meta:
#         model = Candidate_skills
#         fields = [
#             'skill',
#             'rating',
#         ]


class ProfileRegistration_expdetail(forms.ModelForm):
    class Meta:
        model = Candidate_expdetail
        fields = [
            'department',
            'role',
            'job_type',
            'exp_salary',
        ]


class Resumeforming(forms.ModelForm):
    year_experience = forms.CharField(widget=forms.RadioSelect(choices=experience, ))
    resume_type = forms.CharField(widget=forms.RadioSelect(choices=resume, ))

    class Meta:
        model = Resume_order
        fields = [
            'year_experience',
            'resume_type',
        ]
