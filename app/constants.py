from django.db import models


class TextLen(models.IntegerChoices):
    """Максимальная длинна поля."""

    CUR = 3
    PERSONEL_NUMBER = 9
    RARE = 50
    MEDIUM = 100
    WELL_DONE = 255
