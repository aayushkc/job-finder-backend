from django.contrib import admin
from .models import (CustomUser, Recruiter, JobSeeker,
                     Industry,Skills, EducationInfo, 
                     PrefferedJob, RecruiterLeadDetails, GeneratedLeadStatus)
from recruiter.models import RecruiterDetails, Job, JobRequest
admin.site.register(CustomUser)
admin.site.register(Recruiter)
admin.site.register(JobSeeker)
admin.site.register(RecruiterDetails)
admin.site.register(Industry)
admin.site.register(Skills)
admin.site.register(EducationInfo)
admin.site.register(Job)
admin.site.register(PrefferedJob)
admin.site.register(JobRequest)
admin.site.register(RecruiterLeadDetails)
admin.site.register(GeneratedLeadStatus)