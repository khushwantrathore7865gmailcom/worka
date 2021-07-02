from django.contrib import admin
from .models import Employer, Employer_job_Applied, Employer_job, Employer_job_Saved, Employer_job_Like, \
    Employer_jobquestion, Employer_candidate_jobanswer, Employer_profile, Employer_expired_job
# Register your models here.
admin.site.register(Employer)
admin.site.register(Employer_job_Applied)
admin.site.register(Employer_job)
admin.site.register(Employer_job_Saved)
admin.site.register(Employer_job_Like)
admin.site.register(Employer_jobquestion)
admin.site.register(Employer_candidate_jobanswer)
admin.site.register(Employer_profile)
admin.site.register(Employer_expired_job)


