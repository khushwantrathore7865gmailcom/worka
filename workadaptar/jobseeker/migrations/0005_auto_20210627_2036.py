# Generated by Django 3.2.4 on 2021-06-27 15:06

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('jobseeker', '0004_auto_20210619_2244'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='candidate_profile',
            name='birth_day',
        ),
        migrations.AddField(
            model_name='candidate_edu',
            name='end_month',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='candidate_edu',
            name='end_year',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='candidate_edu',
            name='start_month',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='candidate_edu',
            name='start_year',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='candidate_profdetail',
            name='end_month',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='candidate_profdetail',
            name='end_year',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='candidate_profdetail',
            name='start_month',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='candidate_profdetail',
            name='start_year',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='candidate_profile',
            name='birth_date',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='candidate_profile',
            name='birth_month',
            field=models.IntegerField(null=True),
        ),
        migrations.AddField(
            model_name='candidate_profile',
            name='birth_year',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='candidate_edu',
            name='end_date',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='candidate_edu',
            name='start_date',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='candidate_profdetail',
            name='end_date',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='candidate_profdetail',
            name='start_date',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='candidate_profile',
            name='gender',
            field=models.CharField(blank=True, choices=[('Male', 'Male'), ('Female', 'Female'), ('Others', 'Others')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='candidate_profile',
            name='marital_status',
            field=models.CharField(blank=True, choices=[('Single', 'Single'), ('Married ', 'Married')], max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='candidate_profile',
            name='state',
            field=models.CharField(blank=True, choices=[('Andhra Pradesh', 'Andhra Pradesh'), ('Arunachal Pradesh ', 'Arunachal Pradesh '), ('Assam', 'Assam'), ('Bihar', 'Bihar'), ('Chhattisgarh', 'Chhattisgarh'), ('Goa', 'Goa'), ('Gujarat', 'Gujarat'), ('Haryana', 'Haryana'), ('Himachal Pradesh', 'Himachal Pradesh'), ('Jammu and Kashmir ', 'Jammu and Kashmir '), ('Jharkhand', 'Jharkhand'), ('Karnataka', 'Karnataka'), ('Kerala', 'Kerala'), ('Madhya Pradesh', 'Madhya Pradesh'), ('Maharashtra', 'Maharashtra'), ('Manipur', 'Manipur'), ('Meghalaya', 'Meghalaya'), ('Mizoram', 'Mizoram'), ('Nagaland', 'Nagaland'), ('Odisha', 'Odisha'), ('Punjab', 'Punjab'), ('Rajasthan', 'Rajasthan'), ('Sikkim', 'Sikkim'), ('Tamil Nadu', 'Tamil Nadu'), ('Telangana', 'Telangana'), ('Tripura', 'Tripura'), ('Uttar Pradesh', 'Uttar Pradesh'), ('Uttarakhand', 'Uttarakhand'), ('West Bengal', 'West Bengal'), ('Andaman and Nicobar Islands', 'Andaman and Nicobar Islands'), ('Chandigarh', 'Chandigarh'), ('Dadra and Nagar Haveli', 'Dadra and Nagar Haveli'), ('Daman and Diu', 'Daman and Diu'), ('Lakshadweep', 'Lakshadweep'), ('National Capital Territory of Delhi', 'National Capital Territory of Delhi'), ('Puducherry', 'Puducherry')], max_length=255, null=True),
        ),
        migrations.CreateModel(
            name='Candidate_skills',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('skill', models.CharField(max_length=100)),
                ('rating', models.IntegerField()),
                ('user_id', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='user_skill', to='jobseeker.candidate')),
            ],
        ),
    ]
