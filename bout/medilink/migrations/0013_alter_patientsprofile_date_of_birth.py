# Generated by Django 5.1 on 2024-09-07 12:47

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medilink', '0012_patientsprofile_date_of_birth'),
    ]

    operations = [
        migrations.AlterField(
            model_name='patientsprofile',
            name='date_of_birth',
            field=models.DateField(),
        ),
    ]