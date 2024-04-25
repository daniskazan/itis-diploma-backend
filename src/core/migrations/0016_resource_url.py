# Generated by Django 5.0.3 on 2024-03-31 18:12

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0015_resource_commands_alter_command_resource"),
    ]

    operations = [
        migrations.AddField(
            model_name="resource",
            name="url",
            field=models.URLField(
                help_text="URL ресурса(необходим если хотите выполнять команды, например отправлять запросы в БД",
                null=True,
            ),
        ),
    ]
