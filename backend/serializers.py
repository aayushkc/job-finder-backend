from rest_framework import serializers

from django.contrib.auth import get_user_model
from django.contrib.auth.password_validation import validate_password

from phonenumber_field.serializerfields import PhoneNumberField

from .models import (Recruiter, 
                     JobSeeker, 
                     Skills, 
                     RecruiterLeadDetails, GeneratedLeadStatus, 
                     Industry, PrefferedJob, 
                     EducationInfo,PageMeta,
                     Events
                     )
User = get_user_model()

class UserRegistrationSerializer(serializers.ModelSerializer):
    password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )
    confirm_password = serializers.CharField(
        write_only=True,
        required=True,
        style={'input_type': 'password'}
    )

    phone_number = PhoneNumberField(required=False)

    class Meta:
        model = User
        fields = ('username', 'email', 'password', 'confirm_password', 'phone_number')

    def validate(self, attrs):
        # here check password is strong or what! 
        validate_password(attrs.get('password'))

        if attrs.get('password') != attrs.get('confirm_password'):
            raise serializers.ValidationError(('Password and Confirm Password isn\'t equal!'))

        return attrs

    @staticmethod
    def clean_validated_data(validated_data):
        validated_data.pop('confirm_password')  # here delete confirm password because we dont need that
        return validated_data

    @staticmethod
    def create_sub_user(user):
        if user.is_recriuter:
            Recruiter.objects.create(user=user)
        elif user.is_seeker:
            JobSeeker.objects.create(user=user)

    def create(self, validated_data):
        user = self.Meta.model.objects.create_user(**self.clean_validated_data(validated_data))
        self.create_sub_user(user)
        return user

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("id", "username", 'email', "is_verified")

class SkillsSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skills
        fields = '__all__'

class IndustrySerializer(serializers.ModelSerializer):
    title_name = serializers.CharField(source="get_title_display")
    class Meta:
        model = Industry
        fields = ('id','title', 'title_name')


class PrefferedJobSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = PrefferedJob
        fields = ('id','title','icon')

class EducationLevelInfoSerializer(serializers.ModelSerializer):
    education_level_name = serializers.CharField(source="get_education_level_display")
    class Meta:
        model = EducationInfo
        fields = ('id','education_level', 'education_level_name', 'degree_name')

class RecruiterLeadDetailsSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()
    class Meta:
        model = RecruiterLeadDetails
        fields = ['email', 'name', 'phone_number', 'meeting_date', 'meeting_time']
    @staticmethod
    def create_lead_status(lead):
            GeneratedLeadStatus.objects.create(lead=lead)

    def create(self,  validated_data):
        lead = self.Meta.model.objects.create( **validated_data)
        self.create_lead_status(lead)
        return lead


class GeneratedLeadStatusSerializer(serializers.ModelSerializer):
    phone_number = PhoneNumberField()
    class Meta:
        model = GeneratedLeadStatus
        fields = "__all__"
        depth = 1
        


class PageMetaSerializer(serializers.ModelSerializer):
    class Meta:
        model = PageMeta
        fields = "__all__"

class EventsSerializer(serializers.ModelSerializer):
    class Meta:
        model=Events
        fields="__all__"