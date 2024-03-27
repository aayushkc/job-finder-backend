from django.db import models
from backend.models import JobSeeker, Industry, Skills, PrefferedJob
# Create your models here.
class JobSeekerDetails(models.Model):
    user = models.OneToOneField(JobSeeker, on_delete = models.CASCADE, related_name= "seeker_details")
    dob = models.DateField()
    first_name = models.CharField(max_length = 255)
    middle_name = models.CharField(max_length=255, blank = True)
    last_name = models.CharField(max_length=255)
    resume = models.FileField(upload_to='resumes', blank=True)
    profilePic = models.ImageField(upload_to='seekerProfilePic', blank=True, default='default.jpg')
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, related_name = 'seeker_industry')
    skills = models.ManyToManyField(Skills, related_name='seeker_skills')
    prefferd_job = models.ManyToManyField(PrefferedJob, related_name='seeker_prefferd_job')
    location = models.CharField(max_length = 255, blank=True)
    phone = models.PositiveBigIntegerField(blank= True)

    def __str__(self):
        return self.first_name
    


