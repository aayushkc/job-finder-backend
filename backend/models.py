from django.db import models
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from .managers import MyUserManager
from django_resized import ResizedImageField

# Create your models here.
class CustomUser(AbstractBaseUser,PermissionsMixin):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    username = models.CharField(
         verbose_name="Username",
        max_length=255,
    )
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_recriuter = models.BooleanField(default=False)
    is_seeker = models.BooleanField(default = False)
    objects = MyUserManager()

    USERNAME_FIELD = "email"  #this filed (email) is used when loggin in

    def __str__(self):
        return self.email

    def has_perm(self, perm, obj=None):
        "Does the user have a specific permission?"
        # Simplest possible answer: Yes, always
        return True

    def has_module_perms(self, app_label):
        "Does the user have permissions to view the app `app_label`?"
        # Simplest possible answer: Yes, always
        return True

    @property
    def is_staff(self):
        "Is the user a member of staff?"
        # Simplest possible answer: All admins are staff
        return self.is_admin
    


class Recruiter(models.Model):
    user = models.OneToOneField(CustomUser, on_delete = models.CASCADE, related_name='recruiter')

    def __str__(self):
        return self.user.email


class JobSeeker(models.Model):
    user =  models.OneToOneField(CustomUser, on_delete = models.CASCADE, related_name='seeker')

    def __str__(self):
        return self.user.email


class Industry(models.Model):
    AGRICULTURE = 0
    IT = 1
    EDUCATION =2
    ENGINEERING = 3
    INDUSTRY_CHOICES = (
        (AGRICULTURE, 'Agriculture'),
        (IT, "IT"),
        (EDUCATION, "Education"),
        (ENGINEERING, "Engineering")
    )

    title = models.PositiveSmallIntegerField(choices=INDUSTRY_CHOICES)

    def get_title_display(self):
        return dict(self.INDUSTRY_CHOICES).get(self.title, "Unknown")

    def __str__(self):
        return self.get_title_display()

class Skills(models.Model):
    industry = models.ForeignKey(Industry, on_delete=models.CASCADE, related_name='related_name')
    title = models.CharField(max_length=255)
    icon = ResizedImageField(size=[20, 20],upload_to='icons', blank=True, default='default.jpg')
    def __str__(self):
        return self.title
    

class EducationInfo(models.Model):
    NOT_IMPORTANT = 0
    SEE = 1
    HighSchool = 2
    Bachelor =3
    Masters = 4
    PHD = 5
    EDUCATION_LEVEL_CHOICES = (
        (NOT_IMPORTANT, 'not important'),
        (SEE, 'SEE'),
        (HighSchool, "High School"),
        (Bachelor, "Bachelor"),
        (Masters, "Masters"),
        (PHD, "PHD")
    )
    education_level = models.PositiveSmallIntegerField(choices = EDUCATION_LEVEL_CHOICES)
    degree_name = models.CharField(max_length = 255, blank=True)

    def get_education_level_display(self):
        return dict(self.EDUCATION_LEVEL_CHOICES).get(self.education_level, "Unknown")
    
    def __str__(self):
        return self.degree_name
    

class PrefferedJob(models.Model):
    title = models.CharField(max_length=255)
    icon = ResizedImageField(size=[20, 20],upload_to='preffered-job-icons', blank=True, default='default.jpg')
    def __str__(self):
        return self.title
    

class RecruiterLeadDetails(models.Model):
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
    )
    name = models.CharField(max_length = 120)
    phone = models.PositiveBigIntegerField(unique=True)
    meeting_date = models.DateField()
    meeting_time = models.TimeField()

    def __str__(self):
        return self.email
    

class GeneratedLeadStatus(models.Model):

    PENDING = "pending"
    ACCEPTED = 'accepted'
    REJECTED = 'rejected'

    STATUS_CHOICES = (
        (PENDING, 'Pending'),
        (ACCEPTED, "Accepted"),
        (REJECTED, "Rejected")
    )
    lead = models.OneToOneField(RecruiterLeadDetails, on_delete = models.CASCADE, related_name = 'recuiter_lead')
    status = models.CharField(max_length = 10,choices = STATUS_CHOICES, default=PENDING)

    def __str__(self):
        return f"{self.lead.email} ------ Status:{self.status}"

   
class PageMeta(models.Model):
    pageName = models.CharField(max_length=120)
    title = models.TextField()
    description = models.TextField()

    def __str__(self):
        return self.pageName + "---" + self.title
