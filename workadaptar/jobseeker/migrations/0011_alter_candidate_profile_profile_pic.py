# Generated by Django 3.2.4 on 2021-09-12 10:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('jobseeker', '0010_candidate_expdetail_profile_summary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='candidate_profile',
            name='profile_pic',
            field=models.ImageField(default='profile/avatar.png', upload_to='profile/users/%Y/%m/%d/'),
        ),
    ]
