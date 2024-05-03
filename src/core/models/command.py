from django.db import models
from core.mixins import CreatedAtUpdatedAtMixin


class Script(CreatedAtUpdatedAtMixin, models.Model):
    script_name = models.CharField(
        help_text="Название скрипта", default="undefined", null=False, blank=False
    )
    command_description = models.CharField(
        help_text="Описание скрипта для пользователя",
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
        return self.script_name


class CommandParameter(CreatedAtUpdatedAtMixin, models.Model):
    name = models.CharField(help_text="Название параметра")
    description = models.TextField(help_text="Описание параметра")
    field_type = models.CharField(
        default="text",
        help_text="https://developer.mozilla.org/en-US/docs/Web/HTML/Element/input",
    )
    payload_field = models.CharField(
        help_text="По какому ключу будет находиться параметр в payload`е заявки",
        default="F",
    )

    class Meta:
        verbose_name = "Параметр команды"
        verbose_name_plural = "Параметры команды"

    def __str__(self):
        return f"{self.__class__.__name__} ({self.name})"
