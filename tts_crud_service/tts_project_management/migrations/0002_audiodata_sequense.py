# Generated by Django 4.1.2 on 2022-11-15 11:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("tts_project_management", "0001_initial"),
    ]

    operations = [
        migrations.AddField(
            model_name="audiodata",
            name="sequence",
            field=models.IntegerField(null=True),
        ),
    ]
