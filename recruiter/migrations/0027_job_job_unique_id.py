# Generated by Django 5.0.1 on 2024-07-02 06:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruiter', '0026_remove_jobrequest_quiz_jobrequest_quiz_score'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='job_unique_id',
            field=models.UUIDField(editable=False, null=True, unique=True),
        ),
    ]
