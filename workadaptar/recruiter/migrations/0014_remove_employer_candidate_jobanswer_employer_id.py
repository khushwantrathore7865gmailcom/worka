# Generated by Django 3.2.4 on 2021-07-08 14:03

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('recruiter', '0013_remove_employer_jobquestion_employer_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='employer_candidate_jobanswer',
            name='employer_id',
        ),
    ]
