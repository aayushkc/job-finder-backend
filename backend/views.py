from django.shortcuts import render
from django.contrib.auth import get_user_model
from django.contrib import messages
from django.dispatch import Signal
from django.http.response import Http404
from django.core import mail
from django.core.mail import send_mail


from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView
from rest_framework.exceptions import NotAcceptable, ValidationError
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response
from rest_framework import status
import smtplib
from .serializers import UserRegistrationSerializer, SkillsSerializer, RecruiterLeadDetailsSerializer, GeneratedLeadStatusSerializer
from .models import RecruiterLeadDetails, GeneratedLeadStatus, JobSeeker, Skills, CustomUser
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


class RecruiterLeadDetailsView(CreateAPIView):
    serializer_class = RecruiterLeadDetailsSerializer

    def perform_create(self, serializer):
        print(self.request.POST['email'])
        queryset = User.objects.filter(email=self.request.POST['email'])
        if queryset.exists():
            raise ValidationError({"details":'This email already exists'})
        email_subject = 'Metting Scheduled'
        email_message = f"Meeting has been scheduled successfully on {self.request.POST['meeting_date']} at {self.request.POST['meeting_time']}. Our team will reach out to you throgh mail or phone in the next 48 hours."

        try:
                           
            connection = mail.get_connection()
            connection.open()
                            
            mail_status = send_mail(
                email_subject,
                email_message,
                'hiregurkha@gmail.com',  # Replace with your 'from' email
                [self.request.POST['email']],  
                fail_silently=False
                )
            print(mail_status)
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
       

