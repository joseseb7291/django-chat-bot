from django.db import models

## Table for saving Purchase Order details.
class JokeCount(models.Model):
    joke_word = models.TextField()
    user = models.TextField()