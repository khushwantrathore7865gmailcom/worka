from django.contrib import admin
from .models import Candidate,Candidate_profdetail,Candidate_resume,Candidate_edu,Candidate_profile,Candidate_skills,Candidate_expdetail,Resume_order
# Register your models here.
admin.site.register(Candidate)
admin.site.register(Candidate_edu)
admin.site.register(Candidate_skills)
admin.site.register(Candidate_profile)
admin.site.register(Candidate_resume)
admin.site.register(Candidate_profdetail)
admin.site.register(Candidate_expdetail)
admin.site.register(Resume_order)