# Generated by Django 3.2.4 on 2021-07-08 12:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recruiter', '0011_auto_20210708_1713'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employer_job',
            name='job_savelater',
        ),
    ]
