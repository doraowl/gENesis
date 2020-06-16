from django.db import models
from django.conf import settings


class Text(models.Model):
    text = models.TextField(default='')
    name = models.TextField(default='')
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, default=None)


class Test(models.Model):
    name = models.TextField(default='')
    text = models.ForeignKey('Text',
                             on_delete=models.CASCADE, default=None)


class Task(models.Model):
    sentence = models.TextField(default='')
    test = models.ForeignKey('Test',
                             on_delete=models.CASCADE, default=None)
    theme = models.ForeignKey('Theme',
                              on_delete=models.CASCADE, default=None)


class Theme(models.Model):
    name = models.TextField(default='')
    question = models.TextField(default='')


class Option(models.Model):
    answer = models.TextField(default='')
    correctness = models.BooleanField(default=False)
    task = models.ForeignKey('Task',
                             on_delete=models.CASCADE, default=None)
