# Generated by Django 3.2.4 on 2021-12-04 07:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recruiter', '0005_alter_employer_profile_phone'),
    ]

    operations = [
        migrations.CreateModel(
            name='Employer_Subscription',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subscription_interval', models.IntegerField()),
                ('subscribed_on', models.DateTimeField(auto_now_add=True)),
                ('emp_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='recruiter.employer')),
            ],
        ),
    ]
