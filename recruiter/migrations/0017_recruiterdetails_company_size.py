# Generated by Django 5.0.1 on 2024-04-07 08:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruiter', '0016_alter_job_required_years_of_experience'),
    ]

    operations = [
        migrations.AddField(
            model_name='recruiterdetails',
            name='company_size',
            field=models.PositiveSmallIntegerField(choices=[(0, '1-10'), (1, '11-50'), (2, '51-200'), (3, '201-500'), (4, '501-1000'), (5, '1001-5000'), (6, '5001-10000'), (7, '10001+')], default=0),
            preserve_default=False,
        ),
    ]
