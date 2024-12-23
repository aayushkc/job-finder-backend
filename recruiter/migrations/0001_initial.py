# Generated by Django 5.0.1 on 2024-02-06 06:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('backend', '0002_industry'),
    ]

    operations = [
        migrations.CreateModel(
            name='RecruiterDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('logo', models.ImageField(blank=True, default='default.jpg', null=True, upload_to='logos')),
                ('location', models.CharField(max_length=255)),
                ('description', models.TextField()),
                ('phone', models.PositiveIntegerField()),
                ('company_size', models.PositiveIntegerField()),
                ('company_email', models.EmailField(max_length=254)),
                ('company_url', models.URLField()),
                ('industry', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recruiter_industry', to='backend.industry')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='recruiter_details', to='backend.recruiter')),
            ],
        ),
    ]
