from django.shortcuts import render
from django.db.models import Q
from itertools import chain

from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListAPIView, RetrieveAPIView
from rest_framework.exceptions import ValidationError
from rest_framework.response import Response

from backend.permissions import IsUserSeeker, IsSeekerDetailsObjectorReadOnly
from backend.models import JobSeeker

from recruiter.models import JobRequest, Job
from recruiter.serializers import CreateJobRequestSerializer, ReadJobSerializer
from recruiter.customPagination import CustomJobSeekerJobListPagination

from .models import JobSeekerDetails
from .serializers import JobSeekerDetailsSerializer, ReadSeekerDetailsSerializer, RecommendedJobSerializer, ReadJobRequestSerializer

from .recommendation_logic import recommend_jobs_for_seeker
from django.http import JsonResponse

# Create your views here.
class CheckSeekDetail(ListAPIView):
    permission_classes = [IsUserSeeker]
    def get(self, request, *args, **kwargs):
        user = JobSeeker.objects.get(user=request.user)
        queryset = JobSeekerDetails.objects.filter(user=user)
        if queryset.exists():
            self.queryset = JobSeekerDetails.objects.filter(user=user)
        else:
            raise  ValidationError({"details":'Details for this Account Does Not Exits!!!'})
        self.serializer_class = ReadSeekerDetailsSerializer
        return self.list(request, *args, **kwargs)


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
        if self.request.method == "PUT" or self.request.method == "PATCH" :
            print("ENterrereree Write Jobbbbbbbb")
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

class ViewJobRequest(ListAPIView):
    permission_classes = [IsUserSeeker]
    serializer_class = ReadJobRequestSerializer
       
    def get_queryset(self):
        user = self.request.user.seeker
        seeker = JobRequest.objects.filter(job_seeker= user)
        return seeker

class RecommendedJobsAPIView(ListAPIView):
    permission_classes = [IsUserSeeker]
    pagination_class = CustomJobSeekerJobListPagination

    def get_queryset(self):
        seeker = self.request.user  # Assuming the authenticated user is the job seeker
        recommended_jobs = recommend_jobs_for_seeker(seeker)
        applied_job_pks = JobRequest.objects.filter(job_seeker=seeker.seeker, job__in=recommended_jobs).values_list('job__pk', flat=True)
        recommended_job_pks = [job.pk for job in recommended_jobs]
        queryset = Job.objects.filter(pk__in=recommended_job_pks).exclude(pk__in=applied_job_pks)
        return queryset
    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = RecommendedJobSerializer(queryset, many=True, context ={'request':request})
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)
    
class RetriveJob(RetrieveAPIView):
    queryset = Job.objects.all()

    def get_serializer_class(self):
        if self.request.user.is_anonymous:
            return ReadJobSerializer
        else:
            return RecommendedJobSerializer
        
class ListAllJobs(ListAPIView):
    pagination_class = CustomJobSeekerJobListPagination
    def get_queryset(self):
        query_param_industry = self.request.GET.get('industry')
        query_param_skills = self.request.GET.get('skills')
        if query_param_industry and query_param_industry !='null':
            return Job.objects.filter(industry=query_param_industry)
        elif query_param_skills and query_param_skills !='null':
            return Job.objects.filter( required_skills = query_param_skills)
        else:
            return Job.objects.all()
    
    def list(self,request):
        queryset = self.get_queryset()
        serializer = ReadJobSerializer(queryset, many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)