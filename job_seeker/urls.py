from django.urls import path


from .views import CreateJobSeekerDetails, ViewUpdateUserDetails, CreateJobRequest, RecommendedJobsAPIView, RetriveJob, ViewJobRequest, CheckSeekDetail
urlpatterns = [
    path('create-details/', CreateJobSeekerDetails.as_view(), name='create-seeker-details'),
    path('get-update-details/<int:pk>', ViewUpdateUserDetails.as_view(), name='view-update-seeker-details'),
    path('check-seeker-details/', CheckSeekDetail.as_view(), name='check-seeker-details'),

    path('create-job-request/', CreateJobRequest.as_view(), name='create-job-request'),
    path('recommended-jobs/', RecommendedJobsAPIView.as_view(), name='recommended-jobs'),
    path('get-job/<int:pk>', RetriveJob.as_view(), name='get-seeker-jobs-view-id'),
    path('get-job-request/', ViewJobRequest.as_view(), name='get-all-jobs-request'),

]