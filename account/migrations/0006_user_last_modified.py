# Generated by Django 4.1.4 on 2023-01-04 07:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("account", "0005_alter_user_email"),
    ]

    operations = [
        migrations.AddField(
            model_name="user",
            name="last_modified",
            field=models.DateTimeField(auto_now=True),
        ),
    ]
