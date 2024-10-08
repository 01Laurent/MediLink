# Generated by Django 5.1.1 on 2024-09-10 00:07

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('medilink', '0015_appointment_created_at_appointment_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='appointment',
            name='doctor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='doctor_appointments', to='medilink.doctorprofile'),
        ),
        migrations.AlterField(
            model_name='appointment',
            name='patient',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='appointments', to='medilink.patientsprofile'),
        ),
    ]
