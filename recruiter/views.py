from django.shortcuts import render
from django.http import Http404
from django.shortcuts import get_object_or_404

from rest_framework.generics import CreateAPIView, ListAPIView, RetrieveUpdateAPIView, DestroyAPIView
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError
from rest_framework.pagination import  PageNumberPagination

from .serializers import RecruiterDetailsSerializer, JobSerializer, ReadJobSerializer, GetReacuiterProfile
from .customPagination import CustomPagination

from backend.models import Recruiter, CustomUser
from backend.permissions import IsUserRecruiter, IsRecruiterJobObjectOwnerOrReadOnly,IsRecruiterDetailsObjectorReadOnly
from .models import RecruiterDetails, Job


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

class ListJob(ListAPIView):
    permission_classes = [IsUserRecruiter]
    pagination_class = CustomPagination
    
    def list(self, request):
        user = request.user
        recruiter = Recruiter.objects.get(user=user)
        queryset = Job.objects.filter(company=recruiter) 
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
 