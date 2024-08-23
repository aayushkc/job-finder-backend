from django.urls import path

from .views import (RegisterUser, RecruiterLeadDetailsView, 
                    GeneratedLeadStatusView, 
                    ChangeGenertedLeadStatusView,
                    IndustryView,
                    IndustryCreateView,
                    PrefferedJobView,
                    EducationLevelInfoView,
                    PageMetaCreateView,PageMetaUpdateView,PageMetaView,
                    EventsCompletedView,EventsUpcomingView,EventsCreateView,EventsUpdateView,EventsDeleteView,
                    GetAllSkillsWithJob, GetAllPrefferedJobssWithJob
                    )



urlpatterns = [
    path('auth/register/<str:user_type>', view=RegisterUser.as_view(), name='register-user'),
    
    path('generate-recruiter-lead', view=RecruiterLeadDetailsView.as_view(), name='recruiter-lead'),

    path('list-generated-lead', view=GeneratedLeadStatusView.as_view(), name='list-recruiter-lead'),
    path('change-generated-lead-status/<int:pk>', view=ChangeGenertedLeadStatusView.as_view(), name='change-recruiter-lead-status'),

    path('industry/', view=IndustryView.as_view(), name='industry-get'),
    path('create-industry/', view=IndustryCreateView.as_view(), name='industry-create'),

    path('job-preference/', view=PrefferedJobView.as_view(), name='get-job-preference'),
    path('education-level/', view=EducationLevelInfoView.as_view(), name='get-education-level'),

    path("page-meta-view", PageMetaView.as_view(), name="pagemeta-view"),
    path("page-meta-create", PageMetaCreateView.as_view(), name="pagemeta-create"),
    path("page-meta-update/<int:pk>", PageMetaUpdateView.as_view(), name="pagemeta-update"),

    path("events-completed", EventsCompletedView.as_view(), name="event-completed-list-view"),
    path("events-upcoming", EventsUpcomingView.as_view(), name="event-upcoming-list-view"),
    path("event-create", EventsCreateView.as_view(), name="event-create-view"),
    path("event-update/<int:pk>",EventsUpdateView.as_view(), name="event-update-view"),
    path("event-delete/<int:pk>",EventsDeleteView.as_view(), name="event-delete-view"),

    path('all-skills-with-job', GetAllSkillsWithJob.as_view(), name='all-skills-with-job'),
    path('all-prefferedjob-with-job', GetAllPrefferedJobssWithJob.as_view(), name='all-preffered-with-job'),
] 