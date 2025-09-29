from django.db import models


class Country(models.Model):

    name = models.CharField('نام کشور', max_length=50)

    class Meta:
        verbose_name = 'کشور'
        verbose_name_plural = 'کشور'
        ordering = ['name']

    def __str__(self):
        return self.name


class Currency(models.Model):
    title = models.CharField('عنوان', max_length=50)

    class Meta:
        verbose_name = 'ارز'
        verbose_name_plural = 'ارز'

    def __str__(self):
        return self.title
