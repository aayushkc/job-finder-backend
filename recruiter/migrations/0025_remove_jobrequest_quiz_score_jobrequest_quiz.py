# Generated by Django 5.0.1 on 2024-06-30 07:39

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quiz', '0006_jobquiz_quiz_score'),
        ('recruiter', '0024_jobrequest_quiz_score'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='jobrequest',
            name='quiz_score',
        ),
        migrations.AddField(
            model_name='jobrequest',
            name='quiz',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='job_quiz', to='quiz.jobquiz'),
        ),
    ]
