from rest_framework import serializers

from .models import JobSeekerDetails

class JobSeekerDetailsSerializer(serializers.ModelSerializer):

    class Meta:
        model = JobSeekerDetails
        exclude = ('user',)


class ReadSeekerDetailsSerializer(serializers.ModelSerializer):
    first_name = serializers.CharField()
    middle_name = serializers.CharField()
    last_name = serializers.CharField()
    dob = serializers.DateField()
    resume = serializers.FileField()
    
    industry = serializers.StringRelatedField()
    skills = serializers.StringRelatedField(many=True)
    prefferd_job = serializers.StringRelatedField(many=True)

    class Meta:
        model = JobSeekerDetails
        exclude = ('user',)