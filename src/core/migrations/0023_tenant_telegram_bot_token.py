# Generated by Django 5.0.3 on 2024-04-15 15:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0022_user_telegram_id_alter_resource_commands"),
    ]

    operations = [
        migrations.AddField(
            model_name="tenant",
            name="telegram_bot_token",
            field=models.CharField(
                blank=True,
                help_text="Read more: https://core.telegram.org/bots#3-how-do-i-create-a-bot",
                max_length=46,
                null=True,
            ),
        ),
    ]