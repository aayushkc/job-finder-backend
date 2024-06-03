"""
URL configuration for hire_gurkha_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
from backend.views import SkillSetView, SkillSetCreateView, RecruiterLeadDetailsView,SkillSetWithIndustryView
from django.contrib.auth.views import (  
    PasswordResetConfirmView,
    PasswordResetCompleteView
)

from wagtail.admin import urls as wagtailadmin_urls
from wagtail import urls as wagtail_urls
from wagtail.documents import urls as wagtaildocs_urls

from .api import api_router
urlpatterns = [

    path('admin/', admin.site.urls),

    path('', include('backend.urls')),
    path('recruiter/', include('recruiter.urls')),
    path('job-seeker/', include('job_seeker.urls')),
    
    path('cms/', include(wagtailadmin_urls)),
    path('documents/', include(wagtaildocs_urls)),
    path('pages/', include(wagtail_urls)),
    path('api/v2/', api_router.urls),
   # Password Reset Links for the newly created recruiter Accounts
    path('password-reset-confirm/<uidb64>/<token>/', PasswordResetConfirmView.as_view(template_name='users/password_reset_confirm.html'),name='password_reset_confirm'),
    path('password-reset-complete/',PasswordResetCompleteView.as_view(template_name='users/password_reset_complete.html'),name='password_reset_complete'),
   
    # Add and Get Skills Models routes 
    path('skills/', view=SkillSetView.as_view(), name='skills-get'),
    path('create-skills/', view=SkillSetCreateView.as_view(), name='skills-create'),
    path('get-skills/', view=SkillSetWithIndustryView.as_view(), name='skills-with-industry'),

    # JWT Login routes
    path('login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),

     path('api/password_reset/', include('django_rest_passwordreset.urls', namespace='password_reset')),
     path("__debug__/", include("debug_toolbar.urls")),

    

    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
