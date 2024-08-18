from django.db import models
from backend.models import JobSeeker, Industry, Skills, PrefferedJob
from django_resized import ResizedImageField
from phonenumber_field.modelfields import PhoneNumberField
# Create your models here.
class JobSeekerDetails(models.Model):
    user = models.OneToOneField(JobSeeker, on_delete = models.CASCADE, related_name= "seeker_details")
    dob = models.DateField()
    first_name = models.CharField(max_length = 255)
    middle_name = models.CharField(max_length=255, blank = True)
    last_name = models.CharField(max_length=255)
    resume = models.FileField(upload_to='resumes', blank=True)
    profilePic = ResizedImageField(size=[105, 80],upload_to='seekerProfilePic', blank=True, default='default.jpg')
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, related_name = 'seeker_industry')
    skills = models.ManyToManyField(Skills, related_name='seeker_skills')
    prefferd_job = models.ManyToManyField(PrefferedJob, related_name='seeker_prefferd_job')
    location = models.CharField(max_length = 255, blank=True)
    phone = models.PositiveBigIntegerField(blank= True, null=True)
    phone_number = PhoneNumberField(blank=True)

    def __str__(self):
        return self.first_name
    


