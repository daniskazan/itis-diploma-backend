# Generated by Django 5.0.3 on 2024-03-31 12:58

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0014_rename_executing_command_command_executing_pattern"),
    ]

    operations = [
        migrations.AddField(
            model_name="resource",
            name="commands",
            field=models.ManyToManyField(
                related_name="resource_commands", to="core.command"
            ),
        ),
        migrations.AlterField(
            model_name="command",
            name="resource",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="executing_commands",
                to="core.resource",
            ),
        ),
    ]