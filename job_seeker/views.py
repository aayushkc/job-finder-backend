from django.shortcuts import render

from rest_framework.generics import CreateAPIView, RetrieveUpdateAPIView, ListAPIView
from rest_framework.exceptions import ValidationError

from backend.permissions import IsUserSeeker, IsSeekerDetailsObjectorReadOnly
from backend.models import JobSeeker

from recruiter.models import JobRequest
from recruiter.serializers import CreateJobRequestSerializer

from .models import JobSeekerDetails
from .serializers import JobSeekerDetailsSerializer, ReadSeekerDetailsSerializer

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
                
