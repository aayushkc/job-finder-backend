# Generated by Django 5.0.1 on 2024-04-10 06:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruiter', '0017_recruiterdetails_company_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='jobrequest',
            name='applied_on',
            field=models.DateField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='jobrequest',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(0, 'Waiting'), (1, 'Denied'), (2, 'Shortlist')], default=0),
        ),
    ]
