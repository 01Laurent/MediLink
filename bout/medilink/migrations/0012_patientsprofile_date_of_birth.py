# Generated by Django 5.1 on 2024-09-07 12:38

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medilink', '0011_rename_speciality_doctorprofile_specialty_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='patientsprofile',
            name='date_of_birth',
            field=models.DateField(default=datetime.date(2000, 1, 1)),
        ),
    ]
