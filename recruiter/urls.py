from django.urls import path
from .views import (CreateRecruiterDetails, 
                    CreateJob, ListAcceptedJob, 
                    ListPendingJob,
                    RetriveUpdateJob, 
                    DeleteJob, 
                    RetriveUpdateRecruiterDetails,
                    GetRecruiter, GetJobApplicants,
                    ViewSeekerDetails,UpdateJobRequest)
urlpatterns = [

    # Profile Detils Routes
    path("get-recruiter-profile/", GetRecruiter.as_view(), name="get-recruiter-profile"),
    path("recruiter-details/", CreateRecruiterDetails.as_view(), name="get-recruiter-details"),

    #Edit and Get the Recruiter Profile Detaisl Object
    path("view-recruiter-details/<int:pk>", RetriveUpdateRecruiterDetails.as_view(), name="view-recrutier-details"), 
    
    #Endpoints for Job request model
    path("view-recruiter-job-requests/<int:id>", GetJobApplicants.as_view(), name="view-recrutier-details-job-requests"), 
    path("edit-recruiter-job-requests/<int:pk>", UpdateJobRequest.as_view(), name="edit-recrutier-details-job-requests"), 

    
    # Jobs Routes
    path("add-job/", CreateJob.as_view(), name="add-job"),
    path("view-jobs/", ListAcceptedJob.as_view(), name="view-job"),
    path("view-pending-jobs/", ListPendingJob.as_view(), name="view-pending-job"),
    path("get-job/<int:pk>", RetriveUpdateJob.as_view(), name="get-job"), #Edit and Get the Recruiter Object
    path("delete-job/<int:pk>", DeleteJob.as_view(), name="delete-job"),

    path("job-seeker-deatails/<int:pk>", ViewSeekerDetails.as_view(), name="get-seeker-details")
]