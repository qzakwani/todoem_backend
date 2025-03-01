# Generated by Django 4.1.4 on 2023-01-01 18:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name="TaskGroup",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("name", models.CharField(max_length=150)),
                ("purpose", models.CharField(max_length=250)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "creator",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="taskgroup_creator",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TaskGroupTask",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("task", models.TextField()),
                ("completed", models.BooleanField(default=False)),
                ("description", models.TextField(blank=True, null=True)),
                ("comment", models.TextField(blank=True, null=True)),
                ("due", models.DateTimeField(blank=True, null=True)),
                ("last_modified", models.DateTimeField(auto_now=True)),
                ("created_at", models.DateTimeField(auto_now_add=True)),
                (
                    "completed_by",
                    models.ForeignKey(
                        blank=True,
                        null=True,
                        on_delete=django.db.models.deletion.SET_NULL,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "created_by",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        related_name="created_by",
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "taskgroup",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="taskgroup.taskgroup",
                    ),
                ),
            ],
        ),
        migrations.CreateModel(
            name="TaskGroupMember",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("is_admin", models.BooleanField(default=False)),
                ("is_staff", models.BooleanField(default=False)),
                ("date_added", models.DateTimeField(auto_now_add=True)),
                (
                    "member",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to=settings.AUTH_USER_MODEL,
                    ),
                ),
                (
                    "taskgroup",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="taskgroup.taskgroup",
                    ),
                ),
            ],
        ),
        migrations.AddField(
            model_name="taskgroup",
            name="members",
            field=models.ManyToManyField(
                through="taskgroup.TaskGroupMember", to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.AddConstraint(
            model_name="taskgroupmember",
            constraint=models.UniqueConstraint(
                fields=("taskgroup", "member"),
                name="unique_member",
                violation_error_message="lister already added",
            ),
        ),
    ]
