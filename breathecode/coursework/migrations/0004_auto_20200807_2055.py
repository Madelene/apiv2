# Generated by Django 3.1 on 2020-08-07 20:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('coursework', '0003_syllabus_github_url'),
    ]

    operations = [
        migrations.AlterField(
            model_name='syllabus',
            name='github_url',
            field=models.URLField(default=None, max_length=255, null=True),
        ),
    ]
