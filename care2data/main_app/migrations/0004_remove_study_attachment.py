# Generated by Django 5.1.4 on 2024-12-12 22:26

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0003_study_attachment'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='study',
            name='attachment',
        ),
    ]
