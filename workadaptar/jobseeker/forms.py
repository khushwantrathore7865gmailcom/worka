from django import forms
from django.contrib.auth.forms import UserCreationForm
from user_custom.models import User_custom
from .models import Candidate_profile, Candidate_edu, Candidate_profdetail, Candidate_resume, Candidate_skills, \
    Candidate_expdetail, Resume_order, Resume_headline

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
delivery = [
    ("Regular 8 working days", "Regular 8 working days"),
    ("Express 4 working days(1250/-)", "Express 4 working days(1250/-)"),
    ("Super Express 2 working days(2300)", "Super Express 2 working days(2300)"),
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
date = [
    ('01', '01'),
    ('02', '02'),
    ('03', '03'),
    ('04', '04'), ('05', '05'),
    ('06', '06'),
    ('07', '07'),
    ('08', '08'), ('09', '09'),
    ('10', '10'), ('11', '11'), ('12', '12'),
    ('13', '13'), ('14', '14'), ('15', '16'),
    ('17', '17'),
    ('18', '18'),
    ('19', '19'),
    ('20', '20'), ('21', '21'),
    ('22', '22'),
    ('23', '23'),
    ('24', '24'), ('25', '25'),
    ('26', '26'), ('27', '27'), ('28', '28'),
    ('29', '29'), ('30', '30'), ('31', '31'),

]
month = [
    ('01', '01'),
    ('02', '02'),
    ('03', '03'),
    ('04', '04'), ('05', '05'),
    ('06', '06'),
    ('07', '07'),
    ('08', '08'), ('09', '09'),
    ('10', '10'), ('11', '11'), ('12', '12'),
]
year = [
    ('1951', '1951'),
    ('1952', '1952'),
    ('1953', '1953'),
    ('1954', '1954'), ('1955', '1955'),
    ('1956', '1956'),
    ('1957', '1957'),
    ('1958', '1958'), ('1959', '1959'),
    ('1960', '1960'),
    ('1961', '1961'),
    ('1962', '1962'),
    ('1963', '1963'),
    ('1964', '1964'), ('1965', '1965'),
    ('1966', '1966'),
    ('1967', '1967'),
    ('1968', '1968'), ('1969', '1969'),
    ('1970', '1970'),
    ('1971', '1971'),
    ('1972', '1972'),
    ('1973', '1973'),
    ('1974', '1974'), ('1975', '1975'),
    ('1976', '1976'),
    ('1977', '1977'),
    ('1978', '1978'), ('1979', '1979'),
    ('1980', '1980'),
    ('1981', '1981'),
    ('1982', '1982'),
    ('1983', '1983'),
    ('1984', '1984'), ('1985', '1985'),
    ('1986', '1986'),
    ('1987', '1987'),
    ('1988', '1988'), ('1989', '1989'),
    ('1990', '1990'),
    ('1991', '1991'),
    ('1992', '1992'),
    ('1993', '1993'),
    ('1994', '1994'), ('1995', '1995'),
    ('1996', '1996'),
    ('1997', '1997'),
    ('1998', '1998'), ('1999', '1999'),
    ('2000', '2000'),
    ('2001', '2001'),
    ('2002', '2002'),
    ('2003', '2003'),
    ('2004', '2004'), ('2005', '2005'),
    ('2006', '2006'),
    ('2007', '2007'),
    ('2008', '2008'), ('2009', '2009'),
    ('2010', '2010'),
    ('2011', '2011'),
    ('2012', '2012'),
    ('2013', '2013'),
    ('2014', '2014'), ('2015', '2015'),
    ('2016', '2016'),
    ('2017', '2017'),
    ('2018', '2018'), ('2019', '2019'),
    ('2020', '2020'), ('2021', '2021'),

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
        attrs={'placeholder': 'Confirm Password ', 'class': "input100"}))

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
    phone = forms.CharField(max_length=12, required=False, label='Phone number', widget=forms.TextInput(
        attrs={'class': "input100"}))
    birth_date = forms.ChoiceField(choices=date, required=False, label='Birthdate', widget=forms.Select(
        attrs={'class': "input100"}))
    birth_month = forms.ChoiceField(choices=month, required=False, label='Birth month', widget=forms.Select(
        attrs={'class': "input100"}))
    birth_year = forms.ChoiceField(choices=year, required=False, label='Birth year', widget=forms.Select(
        attrs={'class': "input100"}))
    gender = forms.ChoiceField(choices=Gender, required=False, label='Gender', widget=forms.Select(
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
    profile_pic = forms.ImageField(required=False, label='Profile picture', widget=forms.FileInput(
        attrs={'class': "input100"}))

    class Meta:
        model = Candidate_profile
        fields = [
            'profile_pic',
            'phone',
            'birth_date',
            'birth_month',
            'birth_year',
            'gender',
            'address',
            'city',
            'state',
            'marital_status',

        ]


class ProfileRegisterForm_edu(forms.ModelForm):
    institute_name = forms.CharField(max_length=30, required=False, label='institute name', widget=forms.TextInput(
        attrs={'class': "input100 form-control"}))

    course_type = forms.CharField(max_length=30, required=False, label='course type', widget=forms.TextInput(
        attrs={'class': "input100 form-control"}))
    degree = forms.CharField(max_length=30, required=False, label='degree', widget=forms.TextInput(
        attrs={'class': "input100 form-control"}))
    start_date = forms.ChoiceField(choices=date, required=False, label='start date', widget=forms.Select(
        attrs={'class': "input100 form-control"}))
    start_month = forms.ChoiceField(choices=month, required=False, label='start month', widget=forms.Select(
        attrs={'class': "input100 form-control"}))
    start_year = forms.ChoiceField(choices=year, required=False, label='start year', widget=forms.Select(
        attrs={'class': "input100 form-control"}))

    end_date = forms.ChoiceField(choices=date, required=False, label='end date', widget=forms.Select(
        attrs={'class': "input100 form-control"}))
    end_month = forms.ChoiceField(choices=month, required=False, label='end month', widget=forms.Select(
        attrs={'class': "input100 form-control"}))
    end_year = forms.ChoiceField(choices=year, required=False, label='end year', widget=forms.Select(
        attrs={'class': "input100 form-control"}))

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


education = formset_factory(ProfileRegisterForm_edu, extra=1)


class ProfileRegisterForm_resume(forms.ModelForm):
    class Meta:
        model = Candidate_resume
        fields = [
            'resume_link',
        ]


#
class ProfileRegisterForm_profdetail(forms.ModelForm):
    designation = forms.CharField(max_length=30, required=False, label='designation', widget=forms.TextInput(
        attrs={'class': "input100 form-control"}))
    organization = forms.CharField(max_length=30, required=False, label='organization', widget=forms.TextInput(
        attrs={'class': "input100 form-control"}))
    salary = forms.CharField(max_length=30, required=False, label='salary', widget=forms.TextInput(
        attrs={'class': "input100 form-control"}))
    start_date = forms.ChoiceField(choices=date, required=False, label='start date', widget=forms.Select(
        attrs={'class': "input100 form-control"}))
    start_month = forms.ChoiceField(choices=month, required=False, label='start month', widget=forms.Select(
        attrs={'class': "input100 form-control"}))
    start_year = forms.ChoiceField(choices=year, required=False, label='start year', widget=forms.Select(
        attrs={'class': "input100 form-control"}))
    # is_current = forms.BooleanField(label='Currently working', widget=forms.CheckboxInput())
    end_date = forms.ChoiceField(choices=date, required=False, label='end date', widget=forms.Select(
        attrs={'class': "input100 form-control"}))
    end_month = forms.ChoiceField(choices=month, required=False, label='end month', widget=forms.Select(
        attrs={'class': "input100 form-control"}))
    end_year = forms.ChoiceField(choices=year, required=False, label='end year', widget=forms.Select(
        attrs={'class': "input100 form-control"}))

    class Meta:
        model = Candidate_profdetail
        fields = [
            'designation',
            'organization',
            'salary',
            'start_date',
            'start_month',
            'start_year',
            # 'is_current',
            'end_date',
            'end_month',
            'end_year',
        ]


profesional = formset_factory(ProfileRegisterForm_profdetail, extra=1)


class ProfileRegisterForm_certificate(forms.ModelForm):
    title = forms.CharField(max_length=30, required=False, label='designation', widget=forms.TextInput(
        attrs={'class': "input100 form-control"}))
    organization = forms.CharField(max_length=30, required=False, label='organization', widget=forms.TextInput(
        attrs={'class': "input100 form-control"}))
    detail = forms.CharField(max_length=30, required=False, label='salary', widget=forms.TextInput(
        attrs={'class': "input100 form-control"}))

    start_year = forms.ChoiceField(choices=year, required=False, label='start year', widget=forms.Select(
        attrs={'class': "input100 form-control"}))

    end_year = forms.ChoiceField(choices=year, required=False, label='end year', widget=forms.Select(
        attrs={'class': "input100 form-control"}))

    class Meta:
        model = Candidate_profdetail
        fields = [
            'title',
            'organization',
            'detail',

            'start_year',

            'end_year',
        ]


certificate = formset_factory(ProfileRegisterForm_certificate, extra=1)


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


class ProfileRegistration_expdetail(forms.ModelForm):
    class Meta:
        model = Candidate_expdetail
        fields = [
            'department',
            'role',
            'job_type',
            'exp_salary',
        ]


class Resumeforming_Entery(forms.Form):
    delivery_type = forms.CharField(widget=forms.RadioSelect(choices=delivery, attrs={

    }))


class Resumeforming_Mid(forms.Form):
    delivery_type_Mid = forms.CharField(widget=forms.RadioSelect(choices=delivery, attrs={

    }))


class Resumeforming_senior(forms.Form):
    delivery_type_senior = forms.CharField(widget=forms.RadioSelect(choices=delivery, attrs={
        'name': 'Resumeforming_senior',
    }))


class Resumeforming_Executive(forms.Form):
    delivery_type_Executive = forms.CharField(widget=forms.RadioSelect(choices=delivery, attrs={
        'name': 'Resumeforming_Executive',
    }))


class Resume_headlineForm(forms.ModelForm):
    class Meta:
        model = Resume_headline
        fields = [
            'resume_headline'
        ]
