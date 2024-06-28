
from recruiter.customPagination import CustomPagination
from rest_framework import generics
from rest_framework.response import Response
from rest_framework import status

from .serializers import QuizAnswersSerializer,QuizQuestionSerializer,JobQuizSerializer,QuizNameSerializer
from .models import QuizQuestion,QuizAnswers,JobQuiz
from backend.models import Recruiter
from backend.permissions import IsUserRecruiter,IsQuizSetObjectorReadOnly, IsUserSeeker
class CreateQuizObject(generics.CreateAPIView):
    permission_classes = [IsUserRecruiter]
    serializer_class = JobQuizSerializer

    def perform_create(self, serializer):
        user = Recruiter.objects.get(user = self.request.user)
        serializer.save(recruiter=user)

class GetQuizObject(generics.RetrieveUpdateAPIView):
    permission_classes = [IsQuizSetObjectorReadOnly]
    queryset = JobQuiz.objects.all()
    serializer_class = JobQuizSerializer

class GetQuizObjectSeeker(generics.RetrieveAPIView):
    permission_classes = [IsUserSeeker]
    queryset = JobQuiz.objects.all()
    serializer_class = JobQuizSerializer

class ListQuizName(generics.ListAPIView):
    permission_classes = [IsUserRecruiter]
    serializer_class = QuizNameSerializer

    def list(self, request, *args, **kwargs):
        user = Recruiter.objects.get(user=request.user)
        queryset = JobQuiz.objects.filter(recruiter=user)
        serializer = JobQuizSerializer(queryset,many=True)
        return Response(data=serializer.data, status=status.HTTP_200_OK)

class ListQuiz(generics.ListAPIView):
    permission_classes = [IsUserRecruiter]
    pagination_class = CustomPagination

    def list(self, request, *args, **kwargs):
        user = Recruiter.objects.get(user=request.user)
        self.queryset = JobQuiz.objects.filter(recruiter=user)
        serializer = JobQuizSerializer(self.queryset,many=True)
        page = self.paginate_queryset(serializer.data)
        return self.get_paginated_response(page)
        
class DeleteQuizObject(generics.DestroyAPIView):
    queryset = JobQuiz.objects.all()
    serializer_class = JobQuizSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message":"Quiz question deleted successfully"
        })

    def perform_destroy(self, instance):
        instance.delete()


class ListQuizQuestions(generics.ListAPIView):
    queryset = QuizQuestion.objects.all()
    serializer_class = QuizQuestionSerializer

class DeleteQuestionObject(generics.DestroyAPIView):
    queryset = QuizQuestion.objects.all()
    serializer_class = QuizQuestionSerializer

    def destroy(self, request, *args, **kwargs):
        instance = self.get_object()
        self.perform_destroy(instance)
        return Response({
            "message":"Quiz Set deleted successfully"
        })

    def perform_destroy(self, instance):
        instance.delete()


class ListQuizAnswer(generics.ListAPIView):
    queryset = QuizAnswers.objects.all()
    serializer_class = QuizAnswersSerializer