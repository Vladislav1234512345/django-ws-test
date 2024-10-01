from django.db import models
from user.models import User

# Create your models here.
class Worksheet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    class Meta:
        db_table = 'worksheets'
        verbose_name = 'Анкета'
        verbose_name_plural = 'Анкеты'


class Like(models.Model):
    # Класс, который используется для enum поля данной таблицы
    class Type(models.TextChoices):
        #Выборы для enum поля в таблице
        COMMON = 'COMMON', 'Обычный'
        SUPER = 'SUPER', 'Супер'
        MEGA = 'MEGA', 'Мега'

    # Создание поля enum
    type = models.CharField(max_length=6, choices=Type.choices, default=Type.COMMON)
    receiver = models.ForeignKey('Worksheet', on_delete=models.CASCADE, related_name='received_likes')
    sender = models.ForeignKey('Worksheet', on_delete=models.CASCADE, related_name='sent_likes')


    def __str__(self):
        return self.type

    class Meta:
        db_table = 'likes'
        verbose_name = 'Лайк'
        verbose_name_plural = 'Лайки'