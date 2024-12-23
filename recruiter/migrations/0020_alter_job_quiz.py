# Generated by Django 5.0.1 on 2024-06-23 06:22

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0003_alter_quizanswers_quiz_question_and_more'),
        ('recruiter', '0019_job_quiz'),
    ]

    operations = [
        migrations.AlterField(
            model_name='job',
            name='quiz',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='quiz_for_job', to='quiz.jobquiz'),
        ),
    ]
