# Generated by Django 3.2.4 on 2021-08-30 12:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('user_custom', '0002_alter_user_custom_user_name'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user_custom',
            name='username',
            field=models.CharField(default='', max_length=150),
        ),
    ]
