# Generated by Django 5.0.1 on 2024-03-22 08:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruiter', '0008_job_is_job_approved'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruiterdetails',
            name='phone',
            field=models.PositiveBigIntegerField(),
        ),
    ]
