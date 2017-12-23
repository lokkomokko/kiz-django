from django.db import models


class Med(models.Model):


    code = models.CharField(max_length=50, verbose_name='Код болезни')
    sex = models.CharField(max_length=5, choices=(('муж', 'муж'), ('жен', 'жен')), default='муж', verbose_name='Пол' )
    adult = models.IntegerField(verbose_name='Возраст')
    days = models.IntegerField(verbose_name='Число дней')

    def __str__(self):
        return self.code
