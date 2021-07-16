# Generated by Django 3.2.4 on 2021-06-22 18:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobseeker', '0004_auto_20210619_2244'),
        ('recruiter', '0007_auto_20210621_1430'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employer_job_Saved',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('saved_on', models.DateTimeField(auto_now_add=True)),
                ('candidate_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobseeker.candidate')),
                ('job_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recruiter.employer_job')),
            ],
        ),
        migrations.CreateModel(
            name='Employer_job_Like',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('liked_on', models.DateTimeField(auto_now_add=True)),
                ('candidate_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobseeker.candidate')),
                ('job_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recruiter.employer_job')),
            ],
        ),
        migrations.CreateModel(
            name='Employer_job_Applied',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('applied_on', models.DateTimeField(auto_now_add=True)),
                ('candidate_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='jobseeker.candidate')),
                ('job_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recruiter.employer_job')),
            ],
        ),
    ]
