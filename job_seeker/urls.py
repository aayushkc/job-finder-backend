from django.urls import path


from .views import CreateJobSeekerDetails, ViewUpdateUserDetails, CreateJobRequest
urlpatterns = [
    path('create-details/', CreateJobSeekerDetails.as_view(), name='create-seeker-details'),
    path('get-update-details/<int:pk>', ViewUpdateUserDetails.as_view(), name='view-update-seeker-details'),

    path('create-job-request/', CreateJobRequest.as_view(), name='create-job-request'),

]