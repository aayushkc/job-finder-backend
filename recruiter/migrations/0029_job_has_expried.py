# Generated by Django 5.0.1 on 2024-07-28 06:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruiter', '0028_alter_job_job_unique_id'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='has_expried',
            field=models.BooleanField(default=False),
        ),
    ]