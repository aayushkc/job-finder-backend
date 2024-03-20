from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from django.http import request
from .models import JobSeekerDetails
from recruiter.models import Job, JobRequest
from backend.models import JobSeeker
from django.contrib.sites.shortcuts import get_current_site
class JobSeekerDetailsSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    middle_name = serializers.CharField()
    last_name = serializers.CharField()
    dob = serializers.DateField()
    resume = serializers.FileField()
    
    industry = serializers.StringRelatedField()
  

    class Meta:
        model = JobSeekerDetails
        depth = 1
        exclude = ('user',)


class ReadSeekerDetailsSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    middle_name = serializers.CharField()
    last_name = serializers.CharField()
    dob = serializers.DateField()
    resume = serializers.SerializerMethodField("get_resume")
    profilePic = serializers.SerializerMethodField("get_profilePic")
    industry = serializers.StringRelatedField()
    skills = serializers.StringRelatedField(many=True)
    prefferd_job = serializers.StringRelatedField(many=True)

    class Meta:
        model = JobSeekerDetails
        exclude = ('user',)

    def get_profilePic(self,obj):
        return f'http://{get_current_site(request).domain}/media/{obj.profilePic}'
    
    def get_resume(self,obj):
        return f'http://{get_current_site(request).domain}/media/{obj.resume}'


class RecommendedJobSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    description = serializers.CharField()
    required_years_of_experience = serializers.CharField(source="get_required_years_of_experience_display")
    job_location = serializers.CharField()
    salary = serializers.IntegerField()
    number_of_vacancy = serializers.IntegerField()
    work_location_type = serializers.CharField(source= "get_work_location_type_display")
    level = serializers.CharField(source="get_level_display")
    apply_before = serializers.DateField()
    applied = serializers.SerializerMethodField("get_applied_number")
    industry = serializers.StringRelatedField()
    company = serializers.SerializerMethodField('get_company_name')
    company_description = serializers.SerializerMethodField('get_company_description')
    logo = serializers.SerializerMethodField("get_company_logo")
    hasApplied = serializers.SerializerMethodField("get_has_user_applied")
    # education_info = serializers.StringRelatedField(many=True)
    # required_skills = serializers.StringRelatedField(many=True)
    # job_category = serializers.StringRelatedField(many=True)
    class Meta:
        model = Job
        fields = "__all__"
        depth = 1
    def get_company_name(self,obj):
        
        return obj.company.recruiter_details.name
    
    def get_company_description(self,obj):
        return obj.company.recruiter_details.description
    
    def get_company_logo(self,obj):
        return f'http://{get_current_site(request).domain}/media/{obj.company.recruiter_details.logo}'
    
    def get_applied_number(self,obj):
        return obj.job_request.count()
    
    def get_has_user_applied(self,obj):
        user = JobRequest.objects.filter(job_seeker = self.context['request'].user.seeker,job=obj)
        if user:
            return True
        return False

        
class ReadJobRequestSerializer(serializers.ModelSerializer):
    job = RecommendedJobSerializer()
    class Meta:
        model = JobRequest
        fields = "__all__" 
        depth = 1       
        