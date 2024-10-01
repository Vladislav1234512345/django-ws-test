from django.db import models

from user.models import User

# Create your models here.

class ChatUsers(models.Model):
    user = models.ForeignKey('User', on_delete=models.CASCADE)
    chat = models.ForeignKey('Chat', on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)
    invite_reason = models.CharField(max_length=255)

    class Meta:
        db_table = 'chats_users'
        verbose_name = 'Пользователь чата'
        verbose_name_plural = 'Пользователи чата'


class Chat(models.Model):
    name = models.CharField(verbose_name='Имя чата', max_length=50, null=True, blank=True)
    image = models.ImageField(verbose_name="Изображение чата", upload_to='images/', null=True, blank=True)
    is_group = models.BooleanField(default=False)
    users = models.ManyToManyField(User, related_name='chats', through='ChatUsers')

    def __str__(self):
        return self.name

    class Meta:
        db_table = 'chats'
        verbose_name = 'Чат'
        verbose_name_plural = 'Чаты'



