from django.db import models
from django.contrib.auth.models import User

class Vendedor(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    conectado = models.BooleanField()
    horario = models.CharField(max_length=200)




class Question(models.Model):
    question_text = models.CharField(max_length=200)
    pub_date = models.DateTimeField('date published')


class Choice(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    choice_text = models.CharField(max_length=200)
    votes = models.IntegerField(default=0)