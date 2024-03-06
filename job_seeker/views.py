from django.shortcuts import render

from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from backend.permissions import IsUserSeeker, IsSeekerDetailsObjectorReadOnly
from backend.models import JobSeeker

from recruiter.models import JobRequest, Job
from recruiter.serializers import CreateJobRequestSerializer
from recruiter.customPagination import CustomJobSeekerJobListPagination

from .models import JobSeekerDetails
from .serializers import JobSeekerDetailsSerializer, ReadSeekerDetailsSerializer, RecommendedJobSerializer

from .recommendation_logic import recommend_jobs_for_seeker
from django.http import JsonResponse

# Create your views here.

class CreateJobSeekerDetails(CreateAPIView):
    permission_classes = [IsUserSeeker]
    queryset = JobSeekerDetails.objects.all()
    serializer_class = JobSeekerDetailsSerializer

    def perform_create(self, serializer):
        user = JobSeeker.objects.get(user=self.request.user)
        queryset =  JobSeekerDetails.objects.filter(user=user)
        if queryset.exists():
            raise ValidationError({"details":'Details for this Account Already Exits!!!'})
        else:
            serializer.save(user=user)

class ViewUpdateUserDetails(RetrieveUpdateAPIView):
    permission_classes = [IsSeekerDetailsObjectorReadOnly]
    queryset = JobSeekerDetails.objects.all()


    def get_serializer_class(self):
        if self.request.method == "PUT":
            return JobSeekerDetailsSerializer
        return ReadSeekerDetailsSerializer
    
class CreateJobRequest(CreateAPIView):
    permission_classes = [IsUserSeeker]
    queryset = JobRequest.objects.all()
    serializer_class = CreateJobRequestSerializer

    def perform_create(self, serializer):
            user = JobSeeker.objects.get(user=self.request.user)
            print(self.request.data['job'])
            queryset =  JobRequest.objects.filter(job_seeker=user, job=self.request.data['job'])
            if queryset.exists():
                raise ValidationError({"details":'Job Request Already Posted!!!'})
            else:
                serializer.save(job_seeker=user)

class RecommendedJobsAPIView(ListAPIView):
    permission_classes = [IsUserSeeker]
    pagination_class = CustomJobSeekerJobListPagination
    def get(self, request, *args, **kwargs):
        seeker = request.user  # Assuming the authenticated user is the job seeker
        recommended_jobs = recommend_jobs_for_seeker(seeker)
        job_request = JobRequest.objects.filter(job__in=recommended_jobs)
        applied_jobs = Job.objects.filter(pk__in = job_request.values_list('job'))
        get_job = Job.objects.exclude(pk__in = applied_jobs)
        serializer = RecommendedJobSerializer(get_job, many=True, context ={'request':request})
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)
    
class RetriveJob(RetrieveAPIView):
    queryset = Job.objects.all()
    serializer_class = RecommendedJobSerializer
    
        
