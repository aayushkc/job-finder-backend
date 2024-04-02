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
    phone = models.PositiveBigIntegerField()
    company_min_size =  models.PositiveSmallIntegerField(default=1)
    company_max_size = models.PositiveSmallIntegerField(default=10)
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
    ZERO_TO_SIX_MONTHS = 4
    SIX_MONTHS_TO_ONE_YEAR = 5
    ONE_YEAR_TO_TWO_YEAR = 6
    TWO_YEAR_TO_THREE_YEAR = 7
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
    salary = models.PositiveBigIntegerField(blank=True, null=True)
    min_salary = models.PositiveBigIntegerField(blank=True, null=True)
    max_salary = models.PositiveBigIntegerField(blank=True, null=True)
    number_of_vacancy = models.PositiveSmallIntegerField()
    work_location_type = models.PositiveSmallIntegerField(choices=WORK_LOCATION_CHOICES)
    level = models.PositiveSmallIntegerField(choices=JOB_LEVEL_CHOICES)
    apply_before = models.DateField()
    is_job_approved = models.BooleanField(default=False)
    company = models.ForeignKey(Recruiter, on_delete=models.CASCADE, related_name = 'job_company')
    industry = models.ForeignKey(Industry, on_delete = models.CASCADE, related_name='job_industry')
    education_info = models.ManyToManyField(EducationInfo, related_name='job_education_info')
    required_skills = models.ManyToManyField(Skills, related_name="jobs_skills")
    job_category = models.ManyToManyField(PrefferedJob, related_name="preffered_job")

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