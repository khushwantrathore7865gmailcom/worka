# Generated by Django 3.2.4 on 2021-09-06 16:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('recruiter', '0002_remove_employer_jobquestion_answer_size'),
    ]

    operations = [
        migrations.AddField(
            model_name='employer_jobquestion',
            name='answer_size',
            field=models.IntegerField(default=10),
        ),
    ]
