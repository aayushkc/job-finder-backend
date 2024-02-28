from django.db import models
from backend.models import Recruiter,Industry, Skills, EducationInfo, PrefferedJob, JobSeeker
from froala_editor.fields import FroalaField
# Create your models here.
class RecruiterDetails(models.Model):
    user = models.OneToOneField(Recruiter, on_delete = models.CASCADE, related_name='recruiter_details')
    name = models.CharField(max_length = 255)
    logo = models.ImageField(upload_to='logos', blank=True, default='default.jpg')
    location = models.CharField(max_length = 255)
    description = FroalaField()
    phone = models.PositiveIntegerField()
    company_size = models.PositiveIntegerField()
    company_email = models.EmailField()
    company_url = models.URLField()
    industry = models.ForeignKey(Industry, on_delete = models.CASCADE, related_name='recruiter_industry')
    

    def __str__(self):
        return self.name

class Job(models.Model):
    NOT_IMPORTANT = 0
    LESS_THAN_THREE = 1
    BETWEEN_THREE_AND_SIX = 2
    MORE_THAN_SIX = 3
    WORK_EXPERIENCE_CHOICES = (
        (NOT_IMPORTANT, 'not important'),
        (LESS_THAN_THREE, 'less than three'),
        (BETWEEN_THREE_AND_SIX, 'between three and six'),
        (MORE_THAN_SIX, 'more than six')
    )
    REMOTE = 0
    ONSITE = 1
    HYBRID = 2
    WORK_LOCATION_CHOICES = (
        (REMOTE, "Remote"),
        (ONSITE, "Onsite"),
        (HYBRID, "Hybrid"),
    )

    INTERN = 0
    FRESHERS = 1
    EXPERIENCED = 2

    JOB_LEVEL_CHOICES = (
        (INTERN, "Intern"),
        (FRESHERS, "Freshers"),
        (EXPERIENCED, "Experienced"),
    )

    title = models.CharField(max_length = 255)
    description = FroalaField()
    required_years_of_experience = models.PositiveSmallIntegerField(choices=WORK_EXPERIENCE_CHOICES)
    job_location = models.CharField(max_length=255, blank=True)
    salary = models.PositiveIntegerField()
    number_of_vacancy = models.PositiveSmallIntegerField()
    work_location_type = models.PositiveSmallIntegerField(choices=WORK_LOCATION_CHOICES)
    level = models.PositiveSmallIntegerField(choices=JOB_LEVEL_CHOICES)
    apply_before = models.DateField()

    company = models.ForeignKey(Recruiter, on_delete=models.CASCADE, related_name = 'job_company')
    industry = models.ForeignKey(Industry, on_delete = models.CASCADE, related_name='job_industry')
    education_info = models.ManyToManyField(EducationInfo, related_name='job_education_info')
    required_skills = models.ManyToManyField(Skills, related_name="jobs_skills")
    job_category = models.ManyToManyField(PrefferedJob, related_name="preffered_job", blank=True)

    def __str__(self):
        return  "--" + self.title
    
class JobRequest(models.Model):
    NOT_SEEN = 0
    SEEN = 1
    SEEN_STATUS_CHOICES = (
        (SEEN, 'seen'),
        (NOT_SEEN, 'not seen')
    )

    WAITING = 0
    DENIED = 1
    STATUS_CHOICES = (
        (WAITING, 'waiting'),
        (DENIED, 'denied')
    )
    job = models.ForeignKey(Job, on_delete = models.PROTECT, related_name= 'job_request')
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.PROTECT, related_name = 'job_seeker_request')

    seen_status = models.PositiveSmallIntegerField(choices=SEEN_STATUS_CHOICES, default=NOT_SEEN)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=WAITING)

    def __str__(self):
        return f"{self.job_seeker} - {self.job}"