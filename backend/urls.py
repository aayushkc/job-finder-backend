from django.urls import path

from .views import (RegisterUser, RecruiterLeadDetailsView, 
                    GeneratedLeadStatusView, 
                    ChangeGenertedLeadStatusView)



urlpatterns = [
    path('auth/register/<str:user_type>', view=RegisterUser.as_view(), name='register-user'),

    path('generate-recruiter-lead', view=RecruiterLeadDetailsView.as_view(), name='recruiter-lead'),

    path('list-generated-lead', view=GeneratedLeadStatusView.as_view(), name='list-recruiter-lead'),
    path('change-generated-lead-status/<int:pk>', view=ChangeGenertedLeadStatusView.as_view(), name='change-recruiter-lead-status'),
  
] 