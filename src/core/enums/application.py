from django.db import models


class ApplicationStatusChoice(models.IntegerChoices):
    IN_PROCESS = 0, "В процессе"
    APPROVED = 1, "Подтверждено"
    RESOLVED = 2, "Решено"
    DENIED = 3, "Отказано"


class ApplicationScopeChoice(models.IntegerChoices):
    READ_SCOPE = 0, "Чтение"
    READ_AND_WRITE_SCOPE = 1, "Чтение и запись"
