# Generated by Django 5.0.1 on 2024-04-11 08:02

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('backend', '0008_alter_customuser_is_seeker_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='skills',
            name='industry',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='related_name', to='backend.industry'),
            preserve_default=False,
        ),
    ]
