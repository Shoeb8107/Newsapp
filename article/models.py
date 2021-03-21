import time
from django.db import models
from account.models import Account

class Article(models.Model):
    headline = models.CharField(max_length=200)
    body = models.CharField(max_length=5000)
    url = models.CharField(max_length=200)
    image = models.CharField(max_length=200)
    category = models.CharField(max_length=100)
    source = models.CharField(max_length=50, default="Unknown Source")
    favourite = models.BooleanField()
    date = models.DateTimeField()

    def __str__(self):
        return self.headline


class Comment(models.Model):
    description = models.CharField(max_length=255)
    person = models.ForeignKey(Account, on_delete = models.CASCADE, related_name='persons')
    post = models.ForeignKey(Article, on_delete = models.CASCADE)

    def __str__(self):
        return f' {self.person}, {self.post}'
