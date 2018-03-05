from __future__ import unicode_literals

from django.db import models
from django.utils import timezone

class Question(models.Model):
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    body = models.TextField()

    def __str__(self):
        return self.title

class Answer(models.Model):
    question = models.ForeignKey('questions.Question', related_name='answers')
    date = models.DateTimeField(default=timezone.now)
    author = models.ForeignKey('auth.User')
    text = models.TextField()
    best_answer = models.BooleanField(default=False)

    def best(self):
        self.best_answer = True
        self.save()

    def __str__(self):
        return self.text
