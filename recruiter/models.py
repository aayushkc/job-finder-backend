from django.db import models
from backend.models import Recruiter,Industry, Skills, EducationInfo, PrefferedJob, JobSeeker
from froala_editor.fields import FroalaField
from django_resized import ResizedImageField
from quiz.models import JobQuiz
# Create your models here.
class RecruiterDetails(models.Model):
    ONE_TO_TEN = 0
    LESS_THAN_TEN = 1
    FIFTY_ONE_TO_TWO_HUNDRED = 2
    TWOHUNDRED_ONE_TO_FIVE_HUNDRED  = 3
    FIVEHUNDRED_ONE_TO_THOUSAND = 4
    ONETHOUSAND_ONE_TO_FIVE_THOUSAND = 5
    FIVETHOUSAND_ONE_TO_TEN_THOUSAND = 6
    MORE_THAN_TEN_THOUSAND_ONE = 7
    COMPANY_SIZES_CHOICES = (
        (ONE_TO_TEN, '1-10'),
        (LESS_THAN_TEN, '11-50'),
        (FIFTY_ONE_TO_TWO_HUNDRED, '51-200'),
        (TWOHUNDRED_ONE_TO_FIVE_HUNDRED, '201-500'),
        (FIVEHUNDRED_ONE_TO_THOUSAND, '501-1000'),
        (ONETHOUSAND_ONE_TO_FIVE_THOUSAND, '1001-5000'),
        (FIVETHOUSAND_ONE_TO_TEN_THOUSAND, '5001-10000'),
        (MORE_THAN_TEN_THOUSAND_ONE, '10001+')
    )
    user = models.OneToOneField(Recruiter, on_delete = models.CASCADE, related_name='recruiter_details')
    name = models.CharField(max_length = 255)
    logo = ResizedImageField(size=[105, 80],upload_to='logos', blank=True, default='default.jpg')
    location = models.CharField(max_length = 255)
    description = FroalaField()
    phone = models.PositiveBigIntegerField()
    company_size = models.PositiveSmallIntegerField(choices=COMPANY_SIZES_CHOICES)
    company_min_size =  models.PositiveSmallIntegerField(default=1)
    company_max_size = models.PositiveSmallIntegerField(default=10)
    company_email = models.EmailField()
    company_url = models.URLField(null=True, blank=True)
    industry = models.ForeignKey(Industry, on_delete = models.CASCADE, related_name='recruiter_industry')
    

    def __str__(self):
        return self.name

class Job(models.Model):
    ZERO_TO_ONE = 0
    LESS_THAN_THREE = 1
    BETWEEN_THREE_AND_SIX = 2
    MORE_THAN_SIX = 3
    ZERO_TO_SIX_MONTHS = 4
    SIX_MONTHS_TO_ONE_YEAR = 5
    ONE_YEAR_TO_TWO_YEAR = 6
    TWO_YEAR_TO_THREE_YEAR = 7
    WORK_EXPERIENCE_CHOICES = (
        (ZERO_TO_ONE, '0-1'),
        (LESS_THAN_THREE, '1-3'),
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
    quiz = models.ForeignKey(JobQuiz,on_delete=models.CASCADE, related_name='quiz_for_job', blank=True, null=True)
    education_info = models.ManyToManyField(EducationInfo, related_name='job_education_info')
    required_skills = models.ManyToManyField(Skills, related_name="jobs_skills")
    job_category = models.ManyToManyField(PrefferedJob, related_name="preffered_job")

    def __str__(self):
        return  "--Job Title: " + self.title + " " + "   --- Comapny: " + self.company.user.username
    
class JobRequest(models.Model):
    NOT_SEEN = 0
    SEEN = 1
    SEEN_STATUS_CHOICES = (
        (SEEN, 'seen'),
        (NOT_SEEN, 'not seen')
    )

    WAITING = 0
    DENIED = 1
    SHORTLIST = 2
    STATUS_CHOICES = (
        (WAITING, 'Waiting'),
        (DENIED, 'Denied'),
        (SHORTLIST, 'Shortlist')
    )
    job = models.ForeignKey(Job, on_delete = models.PROTECT, related_name= 'job_request')
    job_seeker = models.ForeignKey(JobSeeker, on_delete=models.PROTECT, related_name = 'job_seeker_request')
    quiz_score = models.PositiveIntegerField(default=0)
    seen_status = models.PositiveSmallIntegerField(choices=SEEN_STATUS_CHOICES, default=NOT_SEEN)
    status = models.PositiveSmallIntegerField(choices=STATUS_CHOICES, default=WAITING)
    applied_on = models.DateField(auto_now=True)

    def __str__(self):
        return f"{self.job_seeker} - {self.job}"
    
