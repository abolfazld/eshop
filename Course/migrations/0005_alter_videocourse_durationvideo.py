# Generated by Django 3.2.6 on 2021-08-12 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Course', '0004_videocourse_durationvideo'),
    ]

    operations = [
        migrations.AlterField(
            model_name='videocourse',
            name='DurationVideo',
            field=models.CharField(blank=True, max_length=20, null=True),
        ),
    ]
