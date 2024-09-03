from django.contrib.auth import get_user_model
from django.dispatch import Signal
from django.http.response import Http404
from django.core import mail
from django.core.mail import send_mail, EmailMessage
from django.db.models import Case, When, BooleanField
from django.db.models.functions import Now
from django.db import connection
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes,force_str
from django.contrib.sites.shortcuts import get_current_site

from rest_framework.generics import CreateAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, RetrieveAPIView
from rest_framework.views import APIView
from rest_framework.exceptions import NotAcceptable, ValidationError
from rest_framework.permissions import IsAdminUser, IsAuthenticated
from rest_framework.response import Response
from rest_framework import status

from .serializers import (UserRegistrationSerializer, SkillsSerializer, 
                          RecruiterLeadDetailsSerializer, GeneratedLeadStatusSerializer, 
                          IndustrySerializer, PrefferedJobSerializer,
                          EducationLevelInfoSerializer,PageMetaSerializer,
                          EventsSerializer,UserSerializer
                          )
from .models import (GeneratedLeadStatus, 
                    Skills,
                     Industry, PrefferedJob,
                     EducationInfo,PageMeta,
                     Events
                     )
from .signals import user_created
from .permissions import IsUserRecruiter
from recruiter.customPagination import CustomPagination
User = get_user_model()
user_created = Signal()
token_generator = PasswordResetTokenGenerator()
# Create your views here.

def my_custom_sql(table_name, field_name):
    """
    param:table_name -> The name of the table in database to access
    param:field_name -> The name of the column to be selected
    """
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT DISTINCT {field_name} from {table_name}")
        row = cursor.fetchall()

    return row

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
        token = token_generator.make_token(user)
        uid = urlsafe_base64_encode(force_bytes(user.pk))
        current_site = get_current_site(self.request).domain
        reset_link = f"http://localhost:3000/activate/{uid}/{token}"
        email_subject="HireGrukha Account Activation"
        email_message = f"Please activate your account by clicking the link below.<br></br> {reset_link}"
        try:
                           
            connection = mail.get_connection()
            connection.open()
                            
            email = EmailMessage(email_subject, email_message, 'hiregurkhaofficial@gmail.com', [user.email])
            email.content_subtype = "html"
            email.send()
        except Exception as e:
            raise Http404

class ActivateUserAccount(APIView):
     def get_user_from_email_verification_token(self,uidb64, token):
    
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            user = get_user_model().objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,get_user_model().DoesNotExist):
            return None
        if user is not None and token_generator.check_token(user, token):
            return user

        return None

     def get(self, request, uidb64, token):
        user = self.get_user_from_email_verification_token(uidb64, token)
        if user:
             if user.is_verified:
                 return Response(data={"User Already Verified"}, status=status.HTTP_208_ALREADY_REPORTED)
             user.is_verified = True
             user.save()
             return Response(data={"User Verification Successfull"}, status=status.HTTP_200_OK)
        else:
            return Response(data={"User Verification UnSuccessfull"}, status=status.HTTP_400_BAD_REQUEST)
       
class ResendAccountActivationLink(APIView):
    def get(self,request,uidb64):
        print(uidb64)
        try:
            uid = force_str(urlsafe_base64_decode(uidb64))
            print("User id",uid)
            user = User.objects.get(pk=uid)
        except (TypeError, ValueError, OverflowError,get_user_model().DoesNotExist):
            user = None
        if user:
            print("Entereeed")
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            current_site = get_current_site(self.request).domain
            reset_link = f"http://localhost:3000/activate/{uid}/{token}"
            email_subject="HireGrukha Account Activation"
            email_message = f"Please activate your account by clicking the link below.<br></br> {reset_link}"
            try:
                            
                connection = mail.get_connection()
                connection.open()      
                email = EmailMessage(email_subject, email_message, 'hiregurkhaofficial@gmail.com', [user.email])
                email.content_subtype = "html"
                email.send()
                return Response(data={"Email sent Successfully"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(data={"Mail sending error"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response(data={"User not found"}, status=status.HTTP_404_NOT_FOUND)
    
class ResendAccountActivationLinkUsingUserId(APIView):
    def get(self,request,id):
        try:
            user = User.objects.get(pk=id)
        except (TypeError, ValueError, OverflowError,get_user_model().DoesNotExist):
            user = None
        if user:
            print("Entereeed")
            token = token_generator.make_token(user)
            uid = urlsafe_base64_encode(force_bytes(user.pk))
            reset_link = f"http://localhost:3000/activate/{uid}/{token}"
            email_subject="HireGrukha Account Activation"
            email_message = f"Please activate your account by clicking the link below.<br></br> {reset_link}"
            try:
                            
                connection = mail.get_connection()
                connection.open()      
                email = EmailMessage(email_subject, email_message, 'hiregurkhaofficial@gmail.com', [user.email])
                email.content_subtype = "html"
                email.send()
                return Response(data={"Email sent Successfully"}, status=status.HTTP_200_OK)
            except Exception as e:
                return Response(data={"Mail sending error"}, status=status.HTTP_503_SERVICE_UNAVAILABLE)
        return Response(data={"User not found"}, status=status.HTTP_404_NOT_FOUND)
   
class GetUserDetails(RetrieveAPIView):
    permission_classes = [IsAuthenticated]
    queryset = User.objects.all()
    serializer_class = UserSerializer

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
       

class PageMetaView(ListAPIView):
    serializer_class = PageMetaSerializer

    def get_queryset(self):
        pageName = self.request.GET.get('pageName')
        queryset = PageMeta.objects.filter(pageName=pageName)
        return queryset
    
class PageMetaUpdateView(UpdateAPIView):
    permission_classes = [IsUserRecruiter]
    serializer_class = PageMetaSerializer
    queryset = PageMeta.objects.all()
    
class PageMetaCreateView(CreateAPIView):
    permission_classes = [IsUserRecruiter]
    queryset = PageMeta.objects.all()
    serializer_class = PageMetaSerializer

class EventsUpcomingView(ListAPIView):
    queryset = Events.objects.annotate(event_completion_check=Case(When(date__lt=Now(), then=True), default=False, output_field=BooleanField())).filter(event_completion_check=False).order_by('-id')
    serializer_class = EventsSerializer
    pagination_class = CustomPagination

class EventsCompletedView(ListAPIView):
    queryset = Events.objects.annotate(event_completion_check=Case(When(date__lt = Now(), then=True),default=False,output_field=BooleanField())).filter(event_completion_check=True).order_by('-id')
    serializer_class = EventsSerializer
    pagination_class = CustomPagination

class EventsCreateView(CreateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Events.objects.all()
    serializer_class = EventsSerializer

class EventsUpdateView(UpdateAPIView):
    permission_classes = [IsAdminUser]
    queryset = Events.objects.all()
    serializer_class = EventsSerializer

class EventsDeleteView(DestroyAPIView):
    permission_classes = [IsAdminUser]
    queryset = Events.objects.all()
    serializer_class = EventsSerializer


class GetAllSkillsWithJob(ListAPIView):
    qr = my_custom_sql('recruiter_job_required_skills','skills_id')
    skills_id = [id[0] for id in qr]
    queryset = Skills.objects.filter(pk__in = skills_id)
    serializer_class = SkillsSerializer
    
class GetAllPrefferedJobssWithJob(ListAPIView):
    qr = my_custom_sql('recruiter_job_job_category','prefferedjob_id')
    preffered_job_id = [id[0] for id in qr]
    queryset = PrefferedJob.objects.filter(pk__in = preffered_job_id)
    serializer_class = PrefferedJobSerializer
    