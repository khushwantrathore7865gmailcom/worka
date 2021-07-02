from django.contrib import admin
from .models import Candidate,Candidate_profdetail,Candidate_resume,Candidate_edu,Candidate_profile,Candidate_skills
# Register your models here.
admin.site.register(Candidate)
admin.site.register(Candidate_edu)
admin.site.register(Candidate_skills)
admin.site.register(Candidate_profile)
admin.site.register(Candidate_resume)
admin.site.register(Candidate_profdetail)
