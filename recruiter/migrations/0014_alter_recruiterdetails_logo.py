# Generated by Django 5.0.1 on 2024-04-04 11:22

import django_resized.forms
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recruiter', '0013_job_salary_alter_job_max_salary_alter_job_min_salary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruiterdetails',
            name='logo',
            field=django_resized.forms.ResizedImageField(blank=True, crop=None, default='default.jpg', force_format=None, keep_meta=True, quality=-1, scale=None, size=[105, 80], upload_to='logos'),
        ),
    ]
