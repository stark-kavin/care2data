# Generated by Django 5.1.4 on 2024-12-13 01:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main_app', '0005_study_attachment'),
    ]

    operations = [
        migrations.AlterField(
            model_name='study',
            name='attachment',
            field=models.FileField(blank=True, null=True, upload_to='study_attachment'),
        ),
    ]