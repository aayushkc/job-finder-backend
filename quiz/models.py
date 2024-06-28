from django.db import models
from backend.models import Recruiter
# Create your models here.
class JobQuiz(models.Model):
    quiz_name = models.CharField(max_length=120)
    recruiter = models.ForeignKey(Recruiter, on_delete=models.CASCADE, related_name="recruiter_quiz")
    def get_number_of_questions(self):
        cnt =  QuizQuestion.objects.filter(quiz = self).count()
        return cnt

    def __str__(self):
        return self.quiz_name

class QuizQuestion(models.Model):
    question = models.CharField(max_length=255)
    quiz = models.ForeignKey(JobQuiz, on_delete=models.CASCADE, related_name='questions')
    def __str__(self):
        return self.question

class QuizAnswers(models.Model):
    quiz_question = models.ForeignKey(QuizQuestion, on_delete=models.CASCADE, related_name='answers')
    option = models.CharField(max_length=255)
    is_correct = models.BooleanField(default=False)

    def __str__(self):
        return self.option 