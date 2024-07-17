from django.shortcuts import render
from django.http import Http404
from django.core import mail
from django.core.mail import send_mail, EmailMessage

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, DestroyAPIView, RetrieveAPIView, UpdateAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework import status

from .serializers import RecruiterDetailsSerializer, JobSerializer, ReadJobSerializer, GetReacuiterProfile,ViewJobRequestSerializer, CreateJobRequestSerializer
from .customPagination import CustomPagination

from backend.models import Recruiter, CustomUser, JobSeeker
from backend.permissions import IsUserRecruiter, IsRecruiterJobObjectOwnerOrReadOnly,IsRecruiterDetailsObjectorReadOnly,IsRecruiterJobRequestObjectOwnerOrReadOnly
from .models import RecruiterDetails, Job, JobRequest

from job_seeker.models import JobSeekerDetails
from job_seeker.serializers import ReadSeekerDetailsSerializer

# Create your views here.
class GetRecruiter(ListAPIView):
    permission_classes = [IsUserRecruiter]
    def get(self, request, *args, **kwargs):
        user = Recruiter.objects.get(user=request.user)
        queryset = RecruiterDetails.objects.filter(user=user)
        if queryset.exists():
            self.queryset = RecruiterDetails.objects.filter(user=user)
        else:
            raise  ValidationError({"details":'Details for this Account Does Not Exits!!!'})
        self.serializer_class = GetReacuiterProfile
        return self.list(request, *args, **kwargs)

class CreateRecruiterDetails(CreateAPIView):
    # permission_classes = [IsUserRecruiter]
    serializer_class = RecruiterDetailsSerializer

    def perform_create(self,serializer):
        user = self.request.user
        recruiter = Recruiter.objects.get(user=user)
        queryset =  RecruiterDetails.objects.filter(user=recruiter)
        if queryset.exists():
            raise ValidationError({"details":'Details for this Account Already Exits!!!'})
        else:
            serializer.save(user=recruiter)

class RetriveUpdateRecruiterDetails(RetrieveUpdateAPIView):
    queryset = RecruiterDetails.objects.all()
    serializer_class = RecruiterDetailsSerializer
    permission_classes = [IsRecruiterDetailsObjectorReadOnly]




class CreateJob(CreateAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsUserRecruiter]

    def perform_create(self, serializer):
       user = self.request.user
       recruiter = Recruiter.objects.get(user=user)
       serializer.save(company=recruiter)

class ListAcceptedJob(ListAPIView):
    permission_classes = [IsUserRecruiter]
    pagination_class = CustomPagination
    
    def list(self, request):
        user = request.user
        recruiter = Recruiter.objects.get(user=user)
        queryset = Job.objects.filter(company=recruiter, is_job_approved=True).order_by("-id")
        serializer = ReadJobSerializer(queryset, many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)
        
class ListPendingJob(ListAPIView):
    permission_classes = [IsUserRecruiter]
    pagination_class = CustomPagination
    
    def list(self, request):
        user = request.user
        recruiter = Recruiter.objects.get(user=user)
        queryset = Job.objects.filter(company=recruiter, is_job_approved=False) .order_by("-id")
        serializer = ReadJobSerializer(queryset, many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)
        

class RetriveUpdateJob(RetrieveUpdateAPIView):
    permission_classes = [IsRecruiterJobObjectOwnerOrReadOnly]
    queryset = Job.objects.all()

    def get_serializer_class(self):

        if self.request.method == 'PUT':
            return JobSerializer
        return ReadJobSerializer

class DeleteJob(DestroyAPIView):
    serializer_class = JobSerializer
    permission_classes = [IsRecruiterJobObjectOwnerOrReadOnly]
    queryset = Job.objects.all()
    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message":"Job deleted successfully"
        })

    def perform_destroy(self, instance):
        instance.delete()
 

class GetJobApplicants(ListAPIView):
    permission_classes = [IsUserRecruiter]
    pagination_class = CustomPagination

    def get(self, request,id):
        recruiter = Recruiter.objects.get(user=request.user)
        queryset = Job.objects.filter(id=id, company=recruiter)
        jobReq = JobRequest.objects.filter(job__in = queryset)
        serializer = ViewJobRequestSerializer(jobReq, many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)

class ViewSeekerDetails(RetrieveAPIView):
    permission_classes = [IsUserRecruiter]
    queryset = JobSeekerDetails.objects.all()
    serializer_class= ReadSeekerDetailsSerializer
    
class UpdateJobRequest(UpdateAPIView):
    permission_classes = [IsUserRecruiter]
    queryset = JobRequest.objects.all()
    serializer_class = CreateJobRequestSerializer

    def perform_update(self, serializer):
        print(self.request.data['user'])
        print(JobSeeker.objects.get(id=self.request.data['user']).user.email)
        seeker = JobSeeker.objects.get(id=self.request.data['user']).user.email
        job_title = self.request.data['job_title']
        company = self.request.data['company']
        if self.request.data['status'] == '2':
            email_subject = 'Congratulations! Your Job Application has been Accepted'
            email_message = f"""
            Dear, {seeker},<br></br> 
            <p>We are thrilled to inform you that your application for the position of <strong>{job_title} </strong> at <strong>{company}</strong> has been accepted!
            </p>
            
            <p style='margin-top:'0.6em''>Our team was impressed with your skills and experience, and we believe you will be a valuable addition to the company. 
            {company} will reach out to you for further details.
            </p>

            <p style='margin-top:'0.6em''>Congratulations once again, and we look forward to seeing you succeed!</p>

            <h3 style='margin-top:'1em''>Best Regards, </h3>
            <p style='margin-top:'0.2em''>The HireGurkha Team</p>
            <a href="https://hiregurkha.com">HireGrukha.com </a>

            """
        elif self.request.data['status'] == '1':
            email_subject = 'Application Rejeceted'
            email_message = f"""
            Dear, {seeker},<br></br> 
            <p>Thank you for applying for the position of <strong>{job_title} </strong> at <strong>{company}</strong>. We appreciate the time and effort you invested in your application.
            After careful consideration, we regret to inform you that your application has not been successful on this occasion.
            </p>
            
            <p style='margin-top:'0.6em''>Please don't be discouraged by this decision. We encourage you to continue exploring opportunities on HireGurkha.com. 
            New positions are added regularly, and we believe that there are many more opportunities that will suit your skills and experience.
            </p>

            <p style='margin-top:'0.6em''>If you have any questions or need any further information, feel free to reach out to us.</p>

            <p style='margin-top:'0.6em''>Thank you once again for your interest in HireGurkha and for considering <strong>{company}</strong> as your potential employer.</p>
            <h3 style='margin-top:'1em''>Best Regards, </h3>
            <p style='margin-top:'0.2em''>The HireGurkha Team</p>
            <a href="https://hiregurkha.com">HireGrukha.com </a>

            """
        else:
            return super().perform_update(serializer)
        try:
                           
            connection = mail.get_connection()
            connection.open()
                            
            email = EmailMessage(email_subject, email_message, 'hiregurkhaofficial@gmail.com', [seeker])
            email.content_subtype = "html"
            email.send()
        except Exception as e:
            raise Http404
        return super().perform_update(serializer)