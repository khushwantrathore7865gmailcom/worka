# Generated by Django 3.2.4 on 2021-07-30 13:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobseeker', '0004_resume_order'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate_profdetail',
            name='end_date',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='candidate_profdetail',
            name='end_month',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='candidate_profdetail',
            name='end_year',
            field=models.IntegerField(blank=True, null=True),
        ),
    ]
