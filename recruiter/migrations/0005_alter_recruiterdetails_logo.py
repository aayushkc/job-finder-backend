# Generated by Django 5.0.1 on 2024-02-26 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruiter', '0004_jobrequest'),
    ]

    operations = [
        migrations.AlterField(
            model_name='recruiterdetails',
            name='logo',
            field=models.ImageField(blank=True, default='default.jpg', upload_to='logos'),
        ),
    ]
