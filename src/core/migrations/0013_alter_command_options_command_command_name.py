# Generated by Django 5.0.3 on 2024-03-30 17:23

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0012_alter_grant_scope_command"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="command",
            options={
                "verbose_name": "Исполняющая команда на объектом доступа",
                "verbose_name_plural": "Исполняющие команды на объектами доступа",
            },
        ),
        migrations.AddField(
            model_name="command",
            name="command_name",
            field=models.CharField(default="undefined", help_text="Название команды"),
        ),
    ]