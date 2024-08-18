from rest_framework import serializers
from backend.models import Recruiter, JobSeeker, Skills, PrefferedJob
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import RecruiterDetails, Job, JobRequest


from job_seeker.serializers import ReadSeekerDetailsSerializer
from job_seeker.models import JobSeekerDetails

from django.contrib.sites.shortcuts import get_current_site
from django.http import request

from datetime import datetime

class GetReacuiterProfile(serializers.ModelSerializer):
    industry = serializers.StringRelatedField()
    class Meta:
        model = RecruiterDetails
        fields = "__all__"
        
class RecruiterDetailsSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = RecruiterDetails
        exclude = ('user',)
        
class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        exclude = ('company', 'job_unique_id')
     
class GetCompanyNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = RecruiterDetails
        fields = ['name', 'user']


class ReadSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        exclude = ('icon',)

class ReadJobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrefferedJob
        exclude = ('icon',)
class ReadJobSerializer(serializers.ModelSerializer):
   
    description = serializers.CharField()
    required_years_of_experience = serializers.CharField(source="get_required_years_of_experience_display")
   
    number_of_vacancy = serializers.IntegerField()
    work_location_type = serializers.CharField(source= "get_work_location_type_display")
    level = serializers.CharField(source="get_level_display")
    required_skills = ReadSkillsSerializer(many=True)
    job_category = ReadJobCategorySerializer(many=True)
    applied = serializers.IntegerField(source ="job_request_count")
    industry = serializers.StringRelatedField()
    company = serializers.SerializerMethodField('get_company_name')
    company_description = serializers.SerializerMethodField('get_company_description')
    logo = serializers.SerializerMethodField("get_company_logo")
    has_expried = serializers.SerializerMethodField("get_job_expried")

    class Meta:
        model = Job
        fields = "__all__"
        read_only=True
        depth = 1
    def get_company_name(self,obj):
        return obj.company.recruiter_details.name

    def get_company_description(self,obj):
        return obj.company.recruiter_details.description
    
    def get_company_logo(self,obj):
        return f'http://127.0.01:8000/media/{obj.company.recruiter_details.logo}'
    
    def get_job_expried(self,obj):
        return datetime.now().date() > obj.apply_before

    @staticmethod
    def setup_eager_loading(queryset):
        queryset = queryset.select_related('industry','quiz','company__recruiter_details').prefetch_related('required_skills','job_category','education_info')
        return queryset
        
    
class CreateJobRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobRequest
        fields = ["job", "status",'quiz_score','quiz_completion_time']


class ReadSeekerDetailsSerializer(serializers.ModelSerializer):
    
    seeker_details = ReadSeekerDetailsSerializer()
    class Meta:
        model = JobSeeker
        exclude = ('user',)


class ViewJobRequestSerializer(serializers.ModelSerializer):
    job_seeker = ReadSeekerDetailsSerializer()
    quiz_question = serializers.SerializerMethodField('get_no_of_question')
    class Meta:
        model = JobRequest
        fields = ['id','job_seeker','quiz_question', 'quiz_score', 'seen_status', 'status', 'applied_on','quiz_completion_time']
        depth = 1

    def get_no_of_question(self,obj):
        if obj.job.quiz:
             return obj.job.quiz.get_number_of_questions() 
        else:
            return 0

class MyTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['userId'] = user.pk
        token['email'] = user.email
        token["isRecruiter"] = user.is_recriuter
        token["isSeeker"] = user.is_seeker
        token['isSuperAdmin'] = user.is_admin

        return token