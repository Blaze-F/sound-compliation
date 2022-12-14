# Generated by Django 4.1.2 on 2022-11-16 08:31

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ("user", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="TtsProject",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("project_title", models.CharField(max_length=100, unique=True)),
                (
                    "user",
                    models.ForeignKey(
                        db_column="user_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="user.user",
                    ),
                ),
            ],
            options={
                "db_table": "project",
            },
        ),
        migrations.CreateModel(
            name="AudioData",
            fields=[
                ("id", models.AutoField(primary_key=True, serialize=False)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                ("updated_at", models.DateTimeField(auto_now=True)),
                ("text", models.CharField(max_length=255)),
                ("slow", models.BooleanField(default=False)),
                ("name", models.CharField(max_length=255)),
                ("sequence", models.IntegerField(null=True)),
                ("path", models.CharField(max_length=255)),
                (
                    "tts_project",
                    models.ForeignKey(
                        db_column="project_id",
                        on_delete=django.db.models.deletion.CASCADE,
                        to="tts_project_management.ttsproject",
                    ),
                ),
            ],
            options={
                "db_table": "audio_data",
            },
        ),
    ]
