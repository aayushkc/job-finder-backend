from rest_framework.permissions import BasePermission


class IsUserRecruiter(BasePermission):
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_recriuter
    
class IsUserSeeker(BasePermission):
    def has_permission(self, request, view):
        
        return request.user.is_authenticated and request.user.is_seeker
    
    
class IsRecruiterDetailsObjectorReadOnly(IsUserRecruiter,BasePermission):
     def has_object_permission(self, request, view, obj):
        return request.user.is_recriuter and obj.user.user == request.user
     
class IsSeekerDetailsObjectorReadOnly(IsUserSeeker,BasePermission):
     def has_object_permission(self, request, view, obj):
        return request.user.is_seeker and obj.user.user == request.user
     
    
class IsRecruiterJobObjectOwnerOrReadOnly(IsUserRecruiter,BasePermission):
    def has_object_permission(self, request, view, obj):
        print(obj.company.user)
        print(request.user.recruiter)
        return request.user.is_recriuter and obj.company.user == request.user
    
class IsRecruiterJobRequestObjectOwnerOrReadOnly(IsUserRecruiter,BasePermission):
    def has_object_permission(self, request, view, obj):
        print(request.user.recruiter)
        return request.user.is_recriuter and obj.job.company.user == request.user