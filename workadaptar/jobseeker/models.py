from django.db import models

# Create your models here.
from user_custom.models import User_custom
from django.core.validators import RegexValidator

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


class Candidate(models.Model):
    user = models.OneToOneField(User_custom, null=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}"


class Candidate_profile(models.Model):
    user_id = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='user_profile')
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Please enter valid phone number. Correct format is 91XXXXXXXX")
    phone = models.CharField(validators=[phone_regex], max_length=20, blank=True, unique=True)
    birth_date = models.IntegerField(null=True)
    birth_month = models.IntegerField(null=True)
    birth_year = models.IntegerField(null=True)
    gender = models.CharField(choices=Gender, max_length=255, null=True, blank=True)
    address = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=50, blank=True)
    pin = models.IntegerField(null=True)
    url = models.URLField(null=True)
    state = models.CharField(choices=state_choices, max_length=255, null=True, blank=True)
    marital_status = models.CharField(choices=Martial_Status, max_length=255, null=True, blank=True)
    profile_pic = models.ImageField(upload_to="profile/users/%Y/%m/%d/", default='profile/avatar.png')


class Candidate_edu(models.Model):
    user_id = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='user_edu')
    institute_name = models.CharField(max_length=250)
    start_date = models.CharField(choices=date, null=True, max_length=20)
    start_month = models.CharField(choices=month, null=True, max_length=20)
    start_year = models.CharField(choices=year, null=True, max_length=20)
    end_date = models.CharField(choices=date, null=True, blank=True, max_length=20)
    end_month = models.CharField(choices=month, null=True, blank=True, max_length=20)
    end_year = models.CharField(choices=year, null=True, blank=True, max_length=20)
    course_type = models.CharField(max_length=250)
    degree = models.CharField(max_length=250)
    created_on = models.DateTimeField(auto_now_add=True)


class Candidate_profdetail(models.Model):
    user_id = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='user_profdetail')
    designation = models.CharField(max_length=250)
    organization = models.CharField(max_length=250)
    salary = models.CharField(max_length=250)
    start_date = models.CharField(choices=date, null=True, max_length=20)
    start_month = models.CharField(choices=month, null=True, max_length=20)
    start_year = models.CharField(choices=year, null=True, max_length=20)
    end_date = models.CharField(choices=date, null=True, blank=True, max_length=20)
    end_month = models.CharField(choices=month, null=True, blank=True, max_length=20)
    end_year = models.CharField(choices=year, null=True, blank=True, max_length=20)
    is_current = models.BooleanField(default=False)


class Candidate_resume(models.Model):
    user_id = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='user_resume')
    resume_link = models.FileField(upload_to="resume/", blank=True)


class Candidate_certificate(models.Model):
    user_id = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='user_certificate')
    title = models.CharField(max_length=250)
    organization = models.CharField(max_length=250)
    detail = models.CharField(max_length=250)

    start_year = models.CharField(choices=year, null=True, max_length=20)

    end_year = models.CharField(choices=year, null=True, blank=True, max_length=20)


class Candidate_skills(models.Model):
    user_id = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='user_skill')
    skill = models.CharField(max_length=100)
    rating = models.IntegerField()


class Candidate_expdetail(models.Model):
    user_id = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='user_expdetail')
    department = models.CharField(max_length=150, blank=True)
    role = models.CharField(max_length=150, blank=True)
    job_type = models.CharField(choices=job_Type, max_length=255, null=True, blank=True)
    exp_salary = models.CharField(max_length=150, blank=True)
    prefer_location = models.CharField(max_length=150, blank=True)
    Total_Working = models.CharField(max_length=50, blank=True)


class Resume_headline(models.Model):
    user_id = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='resume_headline')
    resume_headline = models.TextField()


#
class Resume_order(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    is_payment_Done = models.BooleanField(default=False)
    year_experience = models.CharField(max_length=1024, null=True)
    delivery_type = models.CharField(max_length=1024, default='Regular 8 working days')
    amount = models.IntegerField(default=250, blank=True)
