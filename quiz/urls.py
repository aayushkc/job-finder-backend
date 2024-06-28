from django.urls import path
from .views import (ListQuizName,
                    ListQuizQuestions, ListQuizAnswer, 
                    CreateQuizObject,GetQuizObject,
                    DeleteQuizObject,
                    ListQuiz,DeleteQuestionObject,
                    GetQuizObjectSeeker)
urlpatterns = [

    path("get-quiz-name", ListQuizName.as_view(), name="get-quiz-name"),
    path("get-all-quiz", ListQuiz.as_view(), name="get-all-quiz"),
    path('create-quiz', CreateQuizObject.as_view(), name='quiz-create'),
    path('get-quiz/<int:pk>', GetQuizObject.as_view(), name='quiz-get-obj'),
    path('delete-quiz/<int:pk>', DeleteQuizObject.as_view(), name='quiz-delete-obj'), 

     path('quiz-questions', ListQuizQuestions.as_view(), name='list-quiz-questions'),
     path('delete-question/<int:pk>', DeleteQuestionObject.as_view(), name='quiz-delete-obj'),

     path('quiz-answers', ListQuizAnswer.as_view(), name='list-quiz-answer'),

     path('get-quiz-seeker/<int:pk>', GetQuizObjectSeeker.as_view(), name='quiz-get-obj-seeker'),
]
