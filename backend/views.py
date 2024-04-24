from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.dispatch import Signal
from django.http.response import Http404
from django.core import mail
from django.core.mail import send_mail


from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, RetrieveAPIView
from rest_framework.exceptions import NotAcceptable, ValidationError
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
import smtplib
from .serializers import (UserRegistrationSerializer, SkillsSerializer, 
                          RecruiterLeadDetailsSerializer, GeneratedLeadStatusSerializer, 
                          IndustrySerializer, PrefferedJobSerializer,
                          EducationLevelInfoSerializer)
from .models import (RecruiterLeadDetails, GeneratedLeadStatus, 
                     JobSeeker, Skills, CustomUser,
                     Industry, PrefferedJob,
                     EducationInfo)
from .signals import user_created

User = get_user_model()
user_created = Signal()
# Create your views here.

class RegisterUser(CreateAPIView):
    serializer_class = UserRegistrationSerializer
    lookup_url_kwarg = "user_type"

    def perform_create(self, serializer):
        user_type = self.kwargs.get(self.lookup_url_kwarg, None)
        if user_type == 'recruiter':
            user = serializer.save(is_recriuter=True)
           
        elif user_type == 'job-seeker':
            user = serializer.save(is_seeker=True)
        else:
            raise NotAcceptable

class SkillSetCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Skills.objects.all()
    serializer_class = SkillsSerializer

class SkillSetView(ListAPIView):
    queryset = Skills.objects.all()
    serializer_class = SkillsSerializer


class SkillSetWithIndustryView(ListAPIView):
    serializer_class = SkillsSerializer
    def get_queryset(self):
        industry =  self.request.GET.get('industry')
        if industry == 'null':
            queryset = Skills.objects.all()
        else:
            queryset = Skills.objects.filter(industry =industry )
        return queryset
    

class IndustryView(ListAPIView):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer

class IndustryCreateView(CreateAPIView):
    queryset = Industry.objects.all()
    serializer_class = IndustrySerializer

class PrefferedJobView(ListAPIView):
    queryset = PrefferedJob.objects.all()
    serializer_class = PrefferedJobSerializer

class EducationLevelInfoView(ListAPIView):
    queryset = EducationInfo.objects.all()
    serializer_class = EducationLevelInfoSerializer

class RecruiterLeadDetailsView(CreateAPIView):
    serializer_class = RecruiterLeadDetailsSerializer

    def perform_create(self, serializer):
        
        print(self.request.data['email'])
        queryset = User.objects.filter(email=self.request.data['email'])
        if queryset.exists():
            raise ValidationError({"details":'This email already exists'})
        email_subject = 'Metting Scheduled'
        email_message = f"Hello, {self.request.data['name']}, the meeting has been scheduled successfully on {self.request.data['meeting_date']} at {self.request.data['meeting_time']}. Our team will reach out to you through mail or phone in the next 48 hours."

        try:
                           
            connection = mail.get_connection()
            connection.open()
                            
            mail_status = send_mail(
                email_subject,
                email_message,
                'hiregurkha@gmail.com',  # Replace with your 'from' email
                [self.request.data['email']],  
                fail_silently=True
                )
            print(mail_status)
            # msg = EmailMultiAlternatives(
            #                 # title:
            #                 email_subject,
            #                 # message:
            #                 email_message,
            #                 # from:
            #                 "noreply@hiregurkha.com",
            #                 # to:
            #                  [self.request.data['email']]
            #                 )
            # msg.send()
            serializer.save()
        except Exception as e:
            raise Http404
    
        

class GeneratedLeadStatusView(ListAPIView):
    queryset = GeneratedLeadStatus.objects.all()
    serializer_class = GeneratedLeadStatusSerializer

class ChangeGenertedLeadStatusView(UpdateAPIView):
    queryset = GeneratedLeadStatus.objects.all()
    serializer_class = GeneratedLeadStatusSerializer

    def perform_update(self, serializer):
        instance = serializer.save()

        # Trigger the signal manually to handle account creation and email sending
        try:
            user_created.send(sender=self.__class__, instance=instance)
    
        except Exception as e:
            # Handle other exceptions, such as SMTP connection error
            return Response({'error': 'Failed to send email. Please try again later.'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

           
        return Response(serializer.data, status=status.HTTP_200_OK)
       

