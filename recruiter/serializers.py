from rest_framework import serializers
from backend.models import Recruiter, JobSeeker
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import RecruiterDetails, Job, JobRequest


from job_seeker.serializers import ReadSeekerDetailsSerializer
from job_seeker.models import JobSeekerDetails

from django.contrib.sites.shortcuts import get_current_site
from django.http import request


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

class ReadJobSerializer(serializers.ModelSerializer):
   
    description = serializers.CharField()
    required_years_of_experience = serializers.CharField(source="get_required_years_of_experience_display")
   
    number_of_vacancy = serializers.IntegerField()
    work_location_type = serializers.CharField(source= "get_work_location_type_display")
    level = serializers.CharField(source="get_level_display")
    
    applied = serializers.SerializerMethodField("get_applied_number")
    industry = serializers.StringRelatedField()
    company = serializers.SerializerMethodField('get_company_name')
    company_description = serializers.SerializerMethodField('get_company_description')
    logo = serializers.SerializerMethodField("get_company_logo")
    # education_info = serializers.StringRelatedField(many=True)
    # required_skills = serializers.StringRelatedField(many=True)
    # job_category = serializers.StringRelatedField(many=True)

    class Meta:
        model = Job
        fields = "__all__"
        depth = 1
    def get_company_name(self,obj):
        print(obj.company)
        return obj.company.recruiter_details.name
    
    def get_applied_number(self,obj):
        return obj.job_request.count()

    def get_company_description(self,obj):
        return obj.company.recruiter_details.description
    
    def get_company_logo(self,obj):
        return f'https://www.media.hiregurkha.com/{obj.company.recruiter_details.logo}'
    
        
    
class CreateJobRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobRequest
        fields = ["job", "status",'quiz_score']


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
        fields = ['id','job_seeker','quiz_question', 'quiz_score', 'seen_status', 'status', 'applied_on']
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
        print(user.email)
        token['userId'] = user.pk
        token['email'] = user.email
        token["isRecruiter"] = user.is_recriuter
        token["isSeeker"] = user.is_seeker
        token['isSuperAdmin'] = user.is_admin

        return token