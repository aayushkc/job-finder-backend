from rest_framework import serializers
from .models import JobQuiz,QuizAnswers,QuizQuestion

class QuizNameSerializer(serializers.ModelSerializer):
    class Meta:
        model = JobQuiz
        fields = "__all__"
class QuizAnswersSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    class Meta:
        model = QuizAnswers
        fields = ['id','option', 'is_correct']

class QuizQuestionSerializer(serializers.ModelSerializer):
    id = serializers.IntegerField(required=False)
    answers = QuizAnswersSerializer(many=True)
    class Meta:
        model = QuizQuestion
        depth = 1
        fields = ['id','question', 'answers']

class JobQuizSerializer(serializers.ModelSerializer):
    questions = QuizQuestionSerializer(many=True)
    no_of_question = serializers.IntegerField(source='get_number_of_questions', read_only=True)
    id = serializers.IntegerField(required=False)
    class Meta:
        model = JobQuiz
        fields = ['id','quiz_name', 'questions', 'no_of_question']
    

    def create(self, validated_data):
        
        questions_data = validated_data.pop('questions')
        job_quiz = JobQuiz.objects.create(**validated_data)

        for question_data in questions_data:
            answers_data = question_data.pop('answers')
            quiz_question = QuizQuestion.objects.create(quiz=job_quiz, **question_data)

            for answer_data in answers_data:
                QuizAnswers.objects.create(quiz_question=quiz_question, **answer_data)
        return job_quiz

    def update(self, instance, validated_data):
        print("Entererererererdddd Update")
        questions_data = validated_data.pop('questions')
        instance.quiz_name = validated_data.get('quiz_name', instance.quiz_name)
        instance.save()

        existing_question_ids = [question.id for question in instance.questions.all()]
        new_question_ids = [question['id'] for question in questions_data if 'id' in question]
        print(new_question_ids)
        # Delete questions that are not in the request
        for question_id in existing_question_ids:
            if question_id not in new_question_ids:
                instance.questions.get(id=question_id).delete()

        for question_data in questions_data:
            question_id = question_data.get('id')
            if question_id:
                question_instance = QuizQuestion.objects.get(id=question_id, quiz=instance)
                question_instance.question = question_data.get('question', question_instance.question)
                question_instance.save()

                answers_data = question_data.pop('answers')
                existing_answer_ids = [answer.id for answer in question_instance.answers.all()]
                new_answer_ids = [answer['id'] for answer in answers_data if 'id' in answer]
                

                # Delete answers that are not in the request
                for answer_id in existing_answer_ids:
                    if answer_id not in new_answer_ids:
                        question_instance.answers.get(id=answer_id).delete()

                for answer_data in answers_data:
                    answer_id = answer_data.get('id')
                    if answer_id and answer_data != '':
                        answer_instance = QuizAnswers.objects.get(id=answer_id, quiz_question=question_instance)
                        answer_instance.option = answer_data.get('option', answer_instance.option)
                        answer_instance.is_correct = answer_data.get('is_correct', answer_instance.is_correct)
                        answer_instance.save()
                    else:
                        QuizAnswers.objects.create(quiz_question=question_instance, **answer_data)
            else:
                answers_data = question_data.pop('answers')
                quiz_question = QuizQuestion.objects.create(quiz=instance, **question_data)
                for answer_data in answers_data:
                    QuizAnswers.objects.create(quiz_question=quiz_question, **answer_data)

        return instance
    