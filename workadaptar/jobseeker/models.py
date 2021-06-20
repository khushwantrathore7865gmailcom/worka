from django.db import models

# Create your models here.
from user_custom.models import User_custom


class Candidate(models.Model):
    user = models.OneToOneField(User_custom,null=True,on_delete=models.CASCADE)
    created_on = models.DateTimeField(auto_now_add=True)
    is_email_verified = models.BooleanField(default=False)


    def __str__(self):
        return f"{self.user.username}"



class Candidate_profile(models.Model):
    user_id = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='user_profile')
    birth_day = models.DateField()
    gender = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    marital_status = models.CharField(max_length=100)
    profile_pic = models.ImageField(upload_to=None)


class Candidate_edu(models.Model):
    user_id = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='user_edu')
    institute_name = models.CharField(max_length=250)
    start_date = models.DateField()
    end_date = models.DateField()
    course_type = models.CharField(max_length=250)
    degree = models.CharField(max_length=250)
    created_on = models.DateTimeField(auto_now_add=True)


# class Institute(models.Model):
#     institute_id = models.IntegerField(primary_key=True)
#     institute_name = models.CharField(max_length=250)
# class Candidate_Institute(models.Model):
# #     institute_id = models.IntegerField(primary_key=True)
#     institute_name = models.CharField(max_length=250)

class Candidate_profdetail(models.Model):
    user_id = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='user_profdetail')
    designation = models.CharField(max_length=250)
    organization = models.CharField(max_length=250)
    salary = models.CharField(max_length=250)
    start_date = models.DateField()
    end_date = models.DateField()


class Candidate_resume(models.Model):
    user_id = models.ForeignKey(Candidate, on_delete=models.CASCADE, related_name='user_resume')
    resume_link = models.FileField()
    coverletter_text = models.CharField(max_length=250)
    coverletter_link = models.FileField()
