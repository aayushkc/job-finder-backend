from rest_framework import serializers
from backend.models import Recruiter
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from .models import RecruiterDetails, Job, JobRequest

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
        exclude = ('company',)
     

class ReadJobSerializer(serializers.ModelSerializer):
    title = serializers.CharField()
    description = serializers.CharField()
    required_years_of_experience = serializers.CharField(source="get_required_years_of_experience_display")
    job_location = serializers.CharField()
    salary = serializers.IntegerField()
    number_of_vacancy = serializers.IntegerField()
    work_location_type = serializers.CharField(source= "get_work_location_type_display")
    level = serializers.CharField(source="get_level_display")
    apply_before = serializers.DateField()

    industry = serializers.StringRelatedField()
    education_info = serializers.StringRelatedField(many=True)
    required_skills = serializers.StringRelatedField(many=True)
    job_category = serializers.StringRelatedField(many=True)

    class Meta:
        model = Job
        exclude = ('company',)
        
    
class CreateJobRequestSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobRequest
        exclude = (
            "job_seeker",
        )
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
       

        return token