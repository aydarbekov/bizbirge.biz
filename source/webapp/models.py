from django.db import models

GROUP_CHOICES = (
    ('medicine', 'Лекарства'),
    ('injection', 'Капельница / уколы'),
    ('finance', 'Финансы'),
    ('auto', 'Авто'),
    ('consultation', 'Консультация'),
    ('another', 'Другое'),
)
TYPE_CHOICES = (
    ('need_help', 'Нужна помошь'),
    ('can_help', 'Могу помочь'),
    ('can_consult', 'Могу проконсультировать'),
)
STATUS_CHOICES = (
    ('active', 'Активный'),
    ('deactivated', 'Деактивированный'),
)


class Ad(models.Model):
    ad_type = models.CharField(max_length=50, choices=TYPE_CHOICES, default=TYPE_CHOICES[0][0], verbose_name="Тема")
    number = models.CharField(max_length=50, verbose_name='Номер телефона')
    city = models.CharField(max_length=50, verbose_name='Город')
    group = models.CharField(max_length=50, choices=GROUP_CHOICES, default=GROUP_CHOICES[0][0], verbose_name="Тема")
    description = models.TextField(max_length=3000, verbose_name='Описание')
    status = models.CharField(max_length=50, choices=STATUS_CHOICES, default=STATUS_CHOICES[0][0], verbose_name='Статус')
    date = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='Дата добавления')

    def __str__(self):
        return f"{self.number} - {self.city} - {self.group} - {self.description}"

    class Meta:
        verbose_name = 'Объявление'
        verbose_name_plural = 'Объявления'

