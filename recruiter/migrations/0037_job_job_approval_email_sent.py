# Generated by Django 5.0.1 on 2024-08-26 10:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruiter', '0036_recruiterdetails_phone_number_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='job',
            name='job_approval_email_sent',
            field=models.BooleanField(default=False),
        ),
    ]