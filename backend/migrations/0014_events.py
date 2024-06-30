# Generated by Django 5.0.1 on 2024-06-10 06:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0013_prefferedjob_icon'),
    ]

    operations = [
        migrations.CreateModel(
            name='Events',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=120)),
                ('date', models.DateField()),
                ('description', models.TextField()),
                ('time', models.TimeField()),
                ('venue', models.CharField(max_length=255)),
                ('completion_status', models.BooleanField(default=False)),
            ],
        ),
    ]