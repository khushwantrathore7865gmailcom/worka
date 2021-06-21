from django.db import models

from jobseeker.models import Candidate
from user_custom.models import User_custom
from django.core.validators import RegexValidator


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
                                 message="Please enter valid phone number. Correct format is 04XXXXXXXX")
    phone = models.CharField(validators=[phone_regex], max_length=20, blank=True)
    company_type = models.CharField(max_length=250, blank=True, )
    company_name = models.CharField(max_length=250, blank=True, )
    company_logo = models.ImageField(blank=True, )


class Employer_job(models.Model):
    employer_id = models.ForeignKey(Employer, on_delete=models.CASCADE)
    job_title = models.CharField(max_length=1250)
    job_description = models.CharField(max_length=1250)
    employment_type = models.CharField(max_length=250)
    job_location = models.CharField(max_length=250)
    job_experience = models.CharField(max_length=250)
    job_savelater = models.BooleanField(default=False)
    created_on = models.DateTimeField(auto_now_add=True)
    is_saved = models.BooleanField(default=False)
    is_liked = models.BooleanField(default=False)
    is_applied = models.BooleanField(default=False)


class Employer_jobquestion(models.Model):
    employer_id = models.ForeignKey(Employer, on_delete=models.CASCADE)
    job_id = models.ForeignKey(Employer_job, on_delete=models.CASCADE)
    question = models.CharField(max_length=1250)


class Employer_candidate_jobanswer(models.Model):
    candidate_id = models.ForeignKey(Candidate, models.CASCADE)
    employer_id = models.ForeignKey(Employer, on_delete=models.CASCADE)

    job_id = models.ForeignKey(Employer_job, on_delete=models.CASCADE)
    question_id = models.ForeignKey(Employer_jobquestion, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1250)


class Employer_job_responses(models.Model):
    employer_id = models.ForeignKey(Employer, on_delete=models.CASCADE)
    job_id = models.ForeignKey(Employer_job, on_delete=models.CASCADE)
    candidate_id = models.ForeignKey(Candidate, models.CASCADE)


class Employer_expired_job(models.Model):
    employer_id = models.ForeignKey(Employer, on_delete=models.CASCADE)
    job_id = models.ForeignKey(Employer_job, on_delete=models.CASCADE)
