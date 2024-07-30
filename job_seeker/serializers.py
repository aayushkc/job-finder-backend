from rest_framework import serializers
from rest_framework.fields import CurrentUserDefault
from django.http import request
from .models import JobSeekerDetails
from recruiter.models import Job, JobRequest
from backend.models import  Skills, PrefferedJob
from datetime import datetime
class JobSeekerDetailsSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = JobSeekerDetails
        exclude = ('user',)


class ReadSeekerDetailsSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    middle_name = serializers.CharField()
    last_name = serializers.CharField()
    dob = serializers.DateField()
    resume = serializers.SerializerMethodField("get_resume")
    profilePic = serializers.SerializerMethodField("get_profilePic")
    # industry = serializers.StringRelatedField()
    # skills = serializers.StringRelatedField(many=True)
    # prefferd_job = serializers.StringRelatedField(many=True)

    class Meta:
        model = JobSeekerDetails
        depth = 1
        exclude = ('user',)

    def get_profilePic(self,obj):
        return f'http://127.0.01:8000/media/{obj.profilePic}'
    
    def get_resume(self,obj):
        return f'http://127.0.01:8000/media/{obj.resume}'

class ReadSkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        exclude = ('icon',)

class ReadJobCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = PrefferedJob
        exclude = ('icon',)

class RecommendedJobSerializer(serializers.ModelSerializer):
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
    hasApplied = serializers.SerializerMethodField("get_has_user_applied")
   
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
   
    def get_has_user_applied(self,obj):
        user = JobRequest.objects.filter(job_seeker = self.context['request'].user.seeker,job=obj)
        if user:
            return True
        return False
    
class JobRequestReadJobSerializer(serializers.Serializer):
   
    title = serializers.CharField()
    required_years_of_experience = serializers.CharField(source="get_required_years_of_experience_display")
    work_location_type = serializers.CharField(source= "get_work_location_type_display")
    class Meta:
        model = Job
        fields = ('title', 'required_years_of_experience','work_location_type')
        
class ReadJobRequestSerializer(serializers.ModelSerializer):
    job = JobRequestReadJobSerializer()
    class Meta:
        model = JobRequest
        fields = "__all__" 
        depth = 1       
        