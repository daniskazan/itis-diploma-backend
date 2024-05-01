from django.db import models
from django.db.models.constraints import UniqueConstraint
from core.mixins import CreatedAtUpdatedAtMixin


class CommandPattern(CreatedAtUpdatedAtMixin, models.Model):
    command_name = models.CharField(
        help_text="Название команды", default="undefined", null=False, blank=False
    )
    command_description = models.CharField(
        help_text="Описание команды для пользователя",
        default="undefined",
        null=False,
        blank=False,
    )
    resource = models.ForeignKey(
        "Resource", on_delete=models.CASCADE, related_name="executing_commands"
    )
    executing_pattern = models.TextField(null=False, blank=False)
    command_parameters = models.ManyToManyField(
        to="CommandParameter", related_name="patterns"
    )

    class Meta:
        verbose_name = "Шаблон скрипта"
        verbose_name_plural = "Шаблоны скриптов"

    def __str__(self):
        return self.command_name


class CommandParameter(CreatedAtUpdatedAtMixin, models.Model):
    name = models.CharField(help_text="Название параметра")
    description = models.TextField(help_text="Описание параметра")

    class Meta:
        verbose_name = "Параметр команды"
        verbose_name_plural = "Параметры команды"

    def __str__(self):
        return f"{self.__class__.__name__} ({self.name})"


class UserCommandParameter(CreatedAtUpdatedAtMixin, models.Model):
    user = models.ForeignKey("User", on_delete=models.CASCADE)
    command_parameter = models.ForeignKey("CommandParameter", on_delete=models.CASCADE)
    command_pattern = models.ForeignKey("CommandPattern", on_delete=models.CASCADE)
    value = models.CharField()

    class Meta:
        verbose_name = "Параметр команды юзера"
        verbose_name_plural = "Параметры команд юзера"
        constraints = [
            UniqueConstraint(
                fields=["user", "command_parameter", "command_pattern"],
                name="user_parameter_pattern_unique",
            )
        ]

    def __str__(self):
        return f"{self.__class__.__name__} ({self.user})"
