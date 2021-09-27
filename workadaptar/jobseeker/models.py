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
    phone = models.CharField(validators=[phone_regex], max_length=20, blank=True,unique=True)
    birth_date = models.IntegerField(null=True)
    birth_month = models.IntegerField(null=True)
    birth_year = models.IntegerField(null=True)
    gender = models.CharField(choices=Gender, max_length=255, null=True, blank=True)
    address = models.CharField(max_length=250, blank=True)
    city = models.CharField(max_length=50, blank=True)
    state = models.CharField(choices=state_choices, max_length=255, null=True, blank=True)
    marital_status = models.CharField(choices=Martial_Status, max_length=255, null=True, blank=True)
    profile_pic = models.ImageField(upload_to="profile/users/%Y/%m/%d/", default='profile/avatar.png')


class Candidate_edu(models.Model):
    user_id = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='user_edu')
    institute_name = models.CharField(max_length=250)
    start_date = models.IntegerField(null=True, blank=True)
    start_month = models.IntegerField(null=True, blank=True)
    start_year = models.IntegerField(null=True, blank=True)
    end_date = models.IntegerField(null=True, blank=True)
    end_month = models.IntegerField(null=True, blank=True)
    end_year = models.IntegerField(null=True, blank=True)
    course_type = models.CharField(max_length=250)
    degree = models.CharField(max_length=250)
    created_on = models.DateTimeField(auto_now_add=True)


class Candidate_profdetail(models.Model):
    user_id = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='user_profdetail')
    designation = models.CharField(max_length=250)
    organization = models.CharField(max_length=250)
    salary = models.CharField(max_length=250)
    start_date = models.IntegerField(null=True)
    start_month = models.IntegerField(null=True)
    start_year = models.IntegerField(null=True)
    end_date = models.IntegerField(null=True, blank=True)
    end_month = models.IntegerField(null=True, blank=True)
    end_year = models.IntegerField(null=True, blank=True)
    is_current = models.BooleanField(default=False)


class Candidate_resume(models.Model):
    user_id = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='user_resume')
    resume_link = models.FileField(upload_to=f"resume/", blank=True)
    coverletter_text = models.CharField(max_length=250)
    coverletter_link = models.FileField(upload_to=f"cover_letter/", blank=True)


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
    Profile_Summary = models.CharField(max_length=50, blank=True)


#
class Resume_order(models.Model):
    candidate = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    is_payment_Done = models.BooleanField(default=False)
    year_experience = models.CharField(max_length=1024, null=True)
    delivery_type = models.CharField(max_length=1024, default='Regular 8 working days')
    amount = models.IntegerField(default=250, blank=True)