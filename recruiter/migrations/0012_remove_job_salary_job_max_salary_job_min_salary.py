# Generated by Django 5.0.1 on 2024-04-01 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruiter', '0011_remove_recruiterdetails_company_size_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='job',
            name='salary',
        ),
        migrations.AddField(
            model_name='job',
            name='max_salary',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='job',
            name='min_salary',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
