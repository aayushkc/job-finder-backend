from django.urls import path
from .views import (CreateRecruiterDetails, 
                    CreateJob, ListJob, 
                    RetriveUpdateJob, 
                    DeleteJob, 
                    RetriveUpdateRecruiterDetails,
                    GetRecruiter)
urlpatterns = [

    # Profile Detils Routes
    path("get-recruiter-profile/", GetRecruiter.as_view(), name="get-recruiter-profile"),
    path("recruiter-details/", CreateRecruiterDetails.as_view(), name="get-recruiter-details"),

    #Edit and Get the Recruiter Profile Detaisl Object
    path("view-recruiter-details/<int:pk>", RetriveUpdateRecruiterDetails.as_view(), name="view-recrutier-details"), 
   
    # Jobs Routes
    path("add-job/", CreateJob.as_view(), name="add-job"),
    path("view-jobs/", ListJob.as_view(), name="view-job"),
    path("get-job/<int:pk>", RetriveUpdateJob.as_view(), name="get-job"), #Edit and Get the Recruiter Object
    path("delete-job/<int:pk>", DeleteJob.as_view(), name="delete-job"),
]