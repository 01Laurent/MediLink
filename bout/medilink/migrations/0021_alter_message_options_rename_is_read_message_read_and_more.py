# Generated by Django 5.1.1 on 2024-09-17 06:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('medilink', '0020_notification'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='message',
            options={'ordering': ['-timestamp']},
        ),
        migrations.RenameField(
            model_name='message',
            old_name='is_read',
            new_name='read',
        ),
        migrations.RenameField(
            model_name='message',
            old_name='receiver',
            new_name='recipient',
        ),
        migrations.RemoveField(
            model_name='message',
            name='encrypted_content',
        ),
    ]
