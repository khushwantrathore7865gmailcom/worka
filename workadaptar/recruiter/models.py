from django.db import models

from jobseeker.models import Candidate
from user_custom.models import User_custom
from django.core.validators import RegexValidator

Emply_Type = [
    ('Part time', 'Part time'),
    ('Full time', 'Full time'),
    ('Internship', 'Internship'),
]


# Create your models here.
class Employer(models.Model):
    user = models.ForeignKey(User_custom, null=True, on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    is_email_verified = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.user.username}"

    # password = models.CharField(max_length=32,widget=forms.PasswordInput)


class Employer_profile(models.Model):
    employer = models.ForeignKey(Employer, on_delete=models.CASCADE)
    phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                                 message="Please enter valid phone number. Correct format is 91XXXXXXXX")
    phone = models.CharField(validators=[phone_regex], max_length=20, blank=True)
    company_type = models.CharField(max_length=250, blank=True, )
    company_name = models.CharField(max_length=250, blank=True, )
    company_logo = models.ImageField(blank=True, )


class Employer_job(models.Model):
    employer_id = models.ForeignKey(Employer, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=100)
    job_description = models.CharField(max_length=1250)
    employment_type = models.CharField(choices=Emply_Type, max_length=25, null=True,
                                       blank=True)  # parttime fulltime internship
    skill = models.CharField(max_length=100,null=True)
    job_location = models.CharField(max_length=50)
    job_experience = models.CharField(max_length=20)

    created_on = models.DateTimeField(auto_now_add=True)

    def get_applied_no(self):
        print(self)
        E = Employer_job_Applied.objects.filter(job_id=self)
        print(E)
        if E is None:
            return 0
        else:
            return E.count()

class Employer_jobquestion(models.Model):
    # employer_id = models.ForeignKey(Employer, on_delete=models.CASCADE)
    job_id = models.ForeignKey(Employer_job, on_delete=models.CASCADE)
    question = models.CharField(max_length=100)


class Employer_candidate_jobanswer(models.Model):
    candidate_id = models.ForeignKey(Candidate, models.CASCADE)
    # employer_id = models.ForeignKey(Employer, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Employer_jobquestion, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1250)


class Employer_expired_job(models.Model):
    employer_id = models.ForeignKey(Employer, on_delete=models.CASCADE)
    job_id = models.ForeignKey(Employer_job, on_delete=models.CASCADE)


class Employer_job_Like(models.Model):
    job_id = models.ForeignKey(Employer_job, on_delete=models.CASCADE)
    candidate_id = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    liked_on = models.DateTimeField(auto_now_add=True)


class Employer_job_Saved(models.Model):
    job_id = models.ForeignKey(Employer_job, on_delete=models.CASCADE)
    candidate_id = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    saved_on = models.DateTimeField(auto_now_add=True)


class Employer_job_Applied(models.Model):
    job_id = models.ForeignKey(Employer_job, on_delete=models.CASCADE)
    candidate_id = models.ForeignKey(Candidate, on_delete=models.CASCADE)
    applied_on = models.DateTimeField(auto_now_add=True)
