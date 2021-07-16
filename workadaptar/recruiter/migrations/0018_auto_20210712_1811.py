# Generated by Django 3.2.4 on 2021-07-12 12:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruiter', '0017_alter_employer_job_applied_is_disqualified'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employer_expired_job',
            name='employer_id',
        ),
        migrations.AddField(
            model_name='employer_expired_job',
            name='created_on',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
    ]
