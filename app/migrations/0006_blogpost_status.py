# Generated by Django 5.0.6 on 2024-06-06 17:18

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0005_alter_userprofile_profile_pic'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='status',
            field=models.CharField(blank=True, choices=[('sumbitted', 'submitted'), ('rejected', 'rejected'), ('reviewing', 'reviewing'), ('accepted', 'accepted')], default='submitted', max_length=55, null=True),
        ),
    ]
